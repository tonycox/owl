from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "PawPatroll AI Hackathon 2025 API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")

    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # Security
    ALLOWED_HOSTS: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    # API
    API_V1_STR: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = Field(default=["*"], env="CORS_ORIGINS")

    # Tools
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GOOGLE_API_KEY: str = Field(default="", env="GOOGLE_API_KEY")

    class Config:
        def __init__(self):
            super().__init__(self)

        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
