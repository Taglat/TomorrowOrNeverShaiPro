import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from loguru import logger
from contextlib import asynccontextmanager
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db, Base, engine
from app.services.telegram_bot import TelegramBot
from app.core.api_schemas import MessageRequest, MessageResponse, MessageAnalysis
from app.services.database_service import DatabaseService
from app.core.schemas import UserMessage

# Create bot instance
bot = TelegramBot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Telegram bot...")
    await bot.start()
    polling_task = asyncio.create_task(bot.run_polling())
    yield
    # Shutdown
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await bot.stop()

app = FastAPI(title="Student Emotional Support Bot", lifespan=lifespan)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "running"}

@app.get("/api/analyze/{message_id}")
async def get_message_analysis(
    message_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get analysis for a specific message"""
    db_service = DatabaseService(db)
    result = await db_service.get_message_with_analysis(message_id)
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )
    
    return result

@app.post("/api/messages")
async def process_message(
    message: MessageRequest,
    user_id: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Process new message and get AI response"""
    try:
        # Create database service
        db_service = DatabaseService(db)
        
        # Save message to database
        saved_message = await db_service.create_message(message.message)
        
        # Process with SHAI service
        user_message = UserMessage(user_id=user_id, message_text=message.message)
        shai_response = await bot.shai_service.process_message(user_message)
        
        # Create analysis object
        analysis = MessageAnalysis(
            emotion=shai_response.emotion,
            risk_level=shai_response.risk_level,
            escalation_required=shai_response.escalation_required,
            response_to_user=shai_response.response_to_user
        )
        
        # Save analysis to database
        await db_service.create_analysis(saved_message.id, analysis)
        
        # Process risk and escalate if needed
        await bot.escalation_service.process_risk(
            message_id=saved_message.id,
            user_id=user_id,
            message=message.message,
            risk_level=shai_response.risk_level,
            emotions=shai_response.emotion,
            escalation_required=shai_response.escalation_required
        )
        
        return MessageResponse(
            message_id=saved_message.id,
            analysis=analysis
        )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)