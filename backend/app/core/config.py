import os
from pydantic_settings import BaseSettings, SettingsConfigDict


DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")


class Settings(BaseSettings):
    app_name: str = "AgentOS"
    app_version: str = "0.1.0"
    environment: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
    )

settings = Settings()