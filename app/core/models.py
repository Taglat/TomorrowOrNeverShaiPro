from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship with analysis
    analysis: Mapped["MessageAnalysisModel"] = relationship(back_populates="message", uselist=False)

class MessageAnalysisModel(Base):
    __tablename__ = "message_analyses"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    message_id: Mapped[str] = mapped_column(String, ForeignKey("messages.id"))
    emotions: Mapped[List[str]] = mapped_column(JSON)
    risk_level: Mapped[str] = mapped_column(String)
    escalation_required: Mapped[bool] = mapped_column(Boolean, default=False)
    response_text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship with message
    message: Mapped[Message] = relationship(back_populates="analysis")