import os
from pydantic_settings import BaseSettings, SettingsConfigDict


DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")


class Settings(BaseSettings):
    app_name: str = "AgentOS"
    app_version: str = "0.1.0"
    environment: str = "development"
    jwt_secret_key: str = "SECRET_KEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "DATABASE_URL"
    gemini_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
