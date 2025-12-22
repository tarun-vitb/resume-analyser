"""
Configuration Management for AI Resume Analyzer
Centralized configuration with environment variable support
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database
    database_url: str = Field(default="sqlite:///./resume_analyzer.db", env="DATABASE_URL")
    
    # Cache Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    enable_cache: bool = Field(default=True, env="ENABLE_CACHE")
    
    # File Upload Configuration
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_extensions: str = Field(default="pdf,docx,doc", env="ALLOWED_EXTENSIONS")
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    
    # Model Configuration
    nlp_model: str = Field(default="all-MiniLM-L6-v2", env="NLP_MODEL")
    prediction_model: str = Field(default="xgboost", env="PREDICTION_MODEL")
    enable_gpu: bool = Field(default=False, env="ENABLE_GPU")
    model_cache_dir: str = Field(default="cache/models", env="MODEL_CACHE_DIR")
    
    # External APIs
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    coursera_api_key: Optional[str] = Field(default=None, env="COURSERA_API_KEY")
    udemy_api_key: Optional[str] = Field(default=None, env="UDEMY_API_KEY")
    
    # CORS Configuration
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:8080", env="CORS_ORIGINS")
    
    # Monitoring and Analytics
    enable_analytics: bool = Field(default=False, env="ENABLE_ANALYTICS")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # Deployment
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed file extensions as a list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"

# Global settings instance
settings = Settings()

# Create necessary directories
def create_directories():
    """Create necessary directories for the application"""
    directories = [
        settings.upload_dir,
        settings.model_cache_dir,
        "cache/embeddings",
        "logs",
        "static"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# Model configuration presets
MODEL_CONFIGS = {
    "fast": {
        "nlp_model": "all-MiniLM-L6-v2",
        "prediction_model": "random_forest",
        "enable_gpu": False,
        "batch_size": 16
    },
    "balanced": {
        "nlp_model": "all-mpnet-base-v2",
        "prediction_model": "xgboost",
        "enable_gpu": False,
        "batch_size": 32
    },
    "accurate": {
        "nlp_model": "all-roberta-large-v1",
        "prediction_model": "gradient_boost",
        "enable_gpu": True,
        "batch_size": 8
    }
}

# API Rate Limiting Configuration
RATE_LIMIT_CONFIG = {
    "requests_per_minute": 60,
    "requests_per_hour": 1000,
    "requests_per_day": 10000
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.log_level,
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "level": settings.log_level,
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

# Feature Flags
FEATURE_FLAGS = {
    "enable_multi_language": False,
    "enable_real_time_analysis": True,
    "enable_batch_processing": True,
    "enable_user_accounts": False,
    "enable_analytics_dashboard": False,
    "enable_api_versioning": True,
    "enable_webhook_notifications": False
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "max_concurrent_analyses": 10,
    "analysis_timeout_seconds": 300,
    "embedding_cache_size": 10000,
    "model_warmup_enabled": True,
    "async_processing_enabled": True
}
