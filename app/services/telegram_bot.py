from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from loguru import logger

from app.core.config import settings
from app.core.schemas import UserMessage, EscalationEvent
from app.services.shai_service import ShaiService

class TelegramBot:
    def __init__(self):
        self.shai_service = ShaiService()
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Initialize escalation service
        from app.services.escalation_service import EscalationService
        self.escalation_service = EscalationService(self.application)
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        welcome_message = ("Привет! Я бот-помощник, который готов выслушать и поддержать вас. "
                         "Вы можете поделиться со мной своими мыслями и чувствами.")
        await update.message.reply_text(welcome_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        try:
            user_message = UserMessage(
                user_id=update.message.from_user.id,
                message_text=update.message.text
            )
            
            # Process message with SHAI service
            shai_response = await self.shai_service.process_message(user_message)
            
            # Send response to user
            await update.message.reply_text(shai_response.response_to_user)
            
            # Process risk and handle escalation if needed
            await self.escalation_service.process_risk(
                message_id=str(update.message.message_id),
                user_id=user_message.user_id,
                message=user_message.message_text,
                risk_level=shai_response.risk_level,
                emotions=shai_response.emotion,
                escalation_required=shai_response.escalation_required
            )
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await update.message.reply_text(
                "Извините, произошла ошибка при обработке сообщения. "
                "Пожалуйста, попробуйте позже."
            )

    async def handle_escalation(self, user_message: UserMessage, risk_level: str, emotions: list[str]):
        """Handle escalation to curators"""
        escalation_event = EscalationEvent(
            user_id=user_message.user_id,
            message=user_message.message_text,
            risk_level=risk_level,
            emotions=emotions,
            timestamp=datetime.now().isoformat()
        )
        
        escalation_message = (
            f"⚠️ ESCALATION ALERT ⚠️\n"
            f"User ID: {escalation_event.user_id}\n"
            f"Risk Level: {escalation_event.risk_level}\n"
            f"Emotions: {', '.join(escalation_event.emotions)}\n"
            f"Message: {escalation_event.message}\n"
            f"Time: {escalation_event.timestamp}"
        )
        
        # Send notification to all curators
        curator_ids = [int(id.strip()) for id in settings.CURATOR_CHAT_IDS.split(",") if id.strip()]
        for curator_id in curator_ids:
            try:
                await self.application.bot.send_message(
                    chat_id=curator_id,
                    text=escalation_message
                )
            except Exception as e:
                logger.error(f"Failed to notify curator {curator_id}: {str(e)}")

    async def start(self):
        """Start the bot"""
        await self.application.initialize()
        await self.application.start()
        
    async def stop(self):
        """Stop the bot"""
        try:
            await self.application.stop()
            await self.application.shutdown()
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            
    async def run_polling(self):
        """Run the bot polling in background"""
        try:
            await self.application.updater.start_polling()
        except Exception as e:
            logger.error(f"Error in polling: {e}")