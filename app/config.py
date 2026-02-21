from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Agent"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://utkarsh:122002@192.168.1.12:5432/test"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"
    TELEGRAM_BOT_TOKEN: str = ""
    
    model_config = {"env_file": ".env"}


settings = Settings()
