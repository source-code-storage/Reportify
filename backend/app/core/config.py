"""
Application configuration using Pydantic settings
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # Project Info
    PROJECT_NAME: str = "Report Writing Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ]

    # Database
    DATABASE_URL: str = "sqlite:///./report_assistant.db"  # Can be overridden in .env
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "report_assistant"
    POSTGRES_PORT: int = 5432

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # S3/MinIO
    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "report-assistant"
    S3_REGION: str = "us-east-1"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".png", ".jpg", ".jpeg"]

    # Celery
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    @property
    def CELERY_BROKER(self) -> str:
        return self.CELERY_BROKER_URL or self.REDIS_URL

    @property
    def CELERY_BACKEND(self) -> str:
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    @property
    def QDRANT_URL(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="allow"
    )


settings = Settings()
