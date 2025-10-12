"""
Configuration Management Module

This module handles all application configuration through environment variables
using Pydantic Settings for validation and type safety.

Environment Variables:
    Database Configuration:
        - DB_HOST: Database host (default: localhost)
        - DB_PORT: Database port (default: 5432)
        - DB_NAME: Database name (default: ghg_platform)
        - DB_USER: Database user (default: ghg_user)
        - DB_PASSWORD: Database password (default: 1234)
    
    Connection Pool Settings:
        - DB_POOL_SIZE: Maximum connections in pool (default: 20)
        - DB_MAX_OVERFLOW: Additional connections beyond pool (default: 10)
        - DB_POOL_TIMEOUT: Connection timeout in seconds (default: 30)
        - DB_POOL_RECYCLE: Connection recycle time in seconds (default: 3600)
    
    Application Settings:
        - API_KEY: Optional API key for authentication
        - LOG_LEVEL: Logging level (default: INFO)

Usage:
    from app.config import settings
    
    print(settings.DB_HOST)
    print(settings.database_url)
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses Pydantic Settings for automatic validation and type conversion.
    Settings can be loaded from environment variables or a .env file.
    
    Attributes:
        DB_HOST: Database server hostname or IP address
        DB_PORT: Database server port number
        DB_NAME: Name of the database to connect to
        DB_USER: Database user for authentication
        DB_PASSWORD: Database password for authentication
        DB_POOL_SIZE: Maximum number of connections in the pool
        DB_MAX_OVERFLOW: Additional connections beyond pool size
        DB_POOL_TIMEOUT: Timeout for getting connection from pool (seconds)
        DB_POOL_RECYCLE: Time before recycling connections (seconds)
        API_KEY: Optional API key for authentication (not currently enforced)
        LOG_LEVEL: Application logging level (DEBUG, INFO, WARNING, ERROR)
        APP_NAME: Application name for display and logging
        APP_VERSION: Current application version
    """
    
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "ghg_platform")
    DB_USER: str = os.getenv("DB_USER", "ghg_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "1234")
    
    # Database Connection Pool Settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # API Configuration
    API_KEY: Optional[str] = os.getenv("API_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Application Settings
    APP_NAME: str = "Carbon Emissions Platform"
    APP_VERSION: str = "1.0.0"
    
    @property
    def database_url(self) -> str:
        """
        Construct PostgreSQL connection URL from configuration.
        
        Returns:
            str: Database connection URL in format:
                 postgresql://user:password@host:port/database
                 
        Example:
            postgresql://ghg_user:1234@localhost:5432/ghg_platform
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
