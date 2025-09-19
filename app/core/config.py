from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str
    
    # SHAI.pro Configuration
    SHAI_API_URL: str = "https://hackathon.shai.pro/api/v1/app/d2f70ec3-7434-4a19-95e6-92fe6231cf5d/incoming/message"
    SHAI_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./shai.db"
    
    # Escalation Configuration
    CURATOR_CHAT_IDS: str
    RISK_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()