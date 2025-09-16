from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str
    
    # SHAI.pro Configuration
    SHAI_API_URL: str
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