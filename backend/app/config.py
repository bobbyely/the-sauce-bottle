"""Configuration settings for the application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database configuration
    DATABASE_URL: str

    # add other requirements here
    # secret key, debug bool etc.

    class Config:
        """Configuration for the settings model."""
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()
