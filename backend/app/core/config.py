"""Enhanced configuration settings for the application."""
import os
from typing import Literal, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment support."""
    
    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # Database configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./saucebottle.db"
    POSTGRES_DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "The Sauce Bottle"
    VERSION: str = "0.1.0"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Testing
    TESTING: bool = False
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database."""
        return "sqlite" in self.DATABASE_URL
    
    @property
    def is_postgresql(self) -> bool:
        """Check if using PostgreSQL database."""
        return "postgresql" in self.DATABASE_URL
    
    @property
    def async_database_url(self) -> str:
        """Get async-compatible database URL."""
        # Ensure async drivers are used
        if "sqlite" in self.DATABASE_URL and "aiosqlite" not in self.DATABASE_URL:
            return self.DATABASE_URL.replace("sqlite:", "sqlite+aiosqlite:")
        elif "postgresql" in self.DATABASE_URL and "asyncpg" not in self.DATABASE_URL:
            # Convert psycopg2 URLs to asyncpg
            url = self.DATABASE_URL.replace("postgresql+psycopg2:", "postgresql+asyncpg:")
            url = url.replace("postgresql:", "postgresql+asyncpg:")
            return url
        return self.DATABASE_URL
    
    @property
    def sync_database_url(self) -> str:
        """Get sync-compatible database URL (for migrations)."""
        # Ensure sync drivers are used
        if "sqlite+aiosqlite" in self.DATABASE_URL:
            return self.DATABASE_URL.replace("sqlite+aiosqlite:", "sqlite:")
        elif "postgresql+asyncpg" in self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgresql+asyncpg:", "postgresql:")
        return self.DATABASE_URL
    
    class Config:
        """Configuration for the settings model."""
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields for flexibility


# Create global settings instance
settings = Settings()


# Development-specific settings
class DevelopmentSettings(Settings):
    """Development environment settings."""
    DATABASE_ECHO: bool = True
    
    class Config:
        env_file = ".env.development"


# Production-specific settings  
class ProductionSettings(Settings):
    """Production environment settings."""
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    
    class Config:
        env_file = ".env.production"


# Load environment-specific settings
def get_settings() -> Settings:
    """Get environment-specific settings."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        return Settings()


# Override global settings if needed
if os.getenv("ENVIRONMENT"):
    settings = get_settings()