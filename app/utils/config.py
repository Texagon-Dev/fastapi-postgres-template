import os
from functools import lru_cache
from dotenv import load_dotenv
from typing import Optional

load_dotenv(override=True)

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Sophie CRM")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG", "False").lower()
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    PIPEDRIVE_API_TOKEN: str = os.getenv("PIPEDRIVE_API_TOKEN")
    PIPEDRIVE_BASE_URL: str = os.getenv("PIPEDRIVE_BASE_URL", "https://api.pipedrive.com/v1")

    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = int(os.getenv("SMTP_PORT", "0")) if os.getenv("SMTP_PORT") else None
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[str] = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: Optional[str] = os.getenv("EMAILS_FROM_NAME", APP_NAME)

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()