import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import Message, MessageAnalysisModel
from app.core.api_schemas import MessageAnalysis, MessageResponse

class DatabaseService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_message(self, content: str) -> Message:
        """Create a new message record"""
        message_id = str(uuid.uuid4())
        message = Message(
            id=message_id,
            content=content
        )
        self.session.add(message)
        await self.session.commit()
        return message

    async def create_analysis(self, message_id: str, analysis: MessageAnalysis) -> MessageAnalysisModel:
        """Create a new message analysis record"""
        analysis_model = MessageAnalysisModel(
            id=str(uuid.uuid4()),
            message_id=message_id,
            emotions=analysis.emotion,
            risk_level=analysis.risk_level,
            escalation_required=analysis.escalation_required,
            response_text=analysis.response_to_user
        )
        self.session.add(analysis_model)
        await self.session.commit()
        return analysis_model

    async def get_message_with_analysis(self, message_id: str) -> MessageResponse:
        """Get message and its analysis"""
        query = select(Message).where(Message.id == message_id).join(MessageAnalysisModel)
        result = await self.session.execute(query)
        message = result.scalar_one_or_none()
        
        if not message or not message.analysis:
            return None
            
        return MessageResponse(
            message_id=message.id,
            analysis=MessageAnalysis(
                emotion=message.analysis.emotions,
                risk_level=message.analysis.risk_level,
                escalation_required=message.analysis.escalation_required,
                response_to_user=message.analysis.response_text
            )
        )