from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FTS API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    
    # Search Configuration
    DEFAULT_SEARCH_LIMIT: int = 20
    DEFAULT_RADIUS_KM: float = 20.0
    DEFAULT_BUFFER_KM: float = 5.0
    SIMILARITY_THRESHOLD: float = 0.15
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
