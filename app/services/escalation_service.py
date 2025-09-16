from datetime import datetime
from enum import Enum
from typing import List
import asyncio
from loguru import logger
from telegram.ext import Application
from app.core.config import settings

class RiskLevel(str, Enum):
    NO_RISK = "NO_RISK"
    LOW_RISK = "LOW_RISK"
    MODERATE_RISK = "MODERATE_RISK"
    HIGH_RISK = "HIGH_RISK"

class EscalationService:
    def __init__(self, telegram_app: Application):
        self.telegram_app = telegram_app
        self.risk_threshold = {
            RiskLevel.NO_RISK: False,
            RiskLevel.LOW_RISK: False,
            RiskLevel.MODERATE_RISK: True,
            RiskLevel.HIGH_RISK: True
        }
    
    def _should_escalate(self, risk_level: str, escalation_required: bool) -> bool:
        """
        Determine if the situation requires escalation based on risk level and escalation flag
        """
        try:
            risk = RiskLevel(risk_level)
            return self.risk_threshold[risk] and escalation_required
        except ValueError:
            logger.error(f"Invalid risk level received: {risk_level}")
            return False

    async def notify_curators(self, message_id: str, user_id: int, message: str, 
                            risk_level: str, emotions: List[str]) -> None:
        """
        Send notification to all curators about high-risk situation
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        notification = (
            "🚨 УВЕДОМЛЕНИЕ О РИСКЕ 🚨\n\n"
            f"Время: {timestamp}\n"
            f"ID сообщения: {message_id}\n"
            f"ID пользователя: {user_id}\n"
            f"Уровень риска: {risk_level}\n"
            f"Эмоции: {', '.join(emotions)}\n\n"
            f"Сообщение пользователя:\n{message}\n\n"
            "⚠️ Требуется внимание куратора!"
        )

        curator_ids = [int(id.strip()) for id in settings.CURATOR_CHAT_IDS.split(",") if id.strip()]
        
        for curator_id in curator_ids:
            try:
                await self.telegram_app.bot.send_message(
                    chat_id=curator_id,
                    text=notification,
                    parse_mode='HTML'
                )
                logger.info(f"Notification sent to curator {curator_id}")
            except Exception as e:
                logger.error(f"Failed to notify curator {curator_id}: {str(e)}")

    async def process_risk(self, message_id: str, user_id: int, message: str,
                          risk_level: str, emotions: List[str], escalation_required: bool) -> None:
        """
        Process risk level and escalate if necessary
        """
        if self._should_escalate(risk_level, escalation_required):
            logger.warning(f"High risk situation detected: {risk_level} for message {message_id}")
            await self.notify_curators(message_id, user_id, message, risk_level, emotions)
        else:
            logger.info(f"No escalation needed for message {message_id} with risk level {risk_level}")
