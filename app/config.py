from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./db.sqlite3"
    
    class Config:
        env_file = ".env"


settings = Settings()
