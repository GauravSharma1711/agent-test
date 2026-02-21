from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Agent"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://utkarsh:122002@192.168.1.12:5432/test"
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o"
    TELEGRAM_BOT_TOKEN: str = ""
    
    model_config = {"env_file": ".env"}


settings = Settings()
