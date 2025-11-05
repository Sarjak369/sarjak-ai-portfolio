"""
Configuration management using pydantic-settings.
Loads environment variables and provides type-safe configuration.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Info
    APP_NAME: str = Field(default="Sarjak's AI Portfolio Assistant")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)

    # API Keys
    # Optional; provide via env when available
    GROQ_API_KEY: Optional[SecretStr] = Field(default=None)

    # Database Configuration
    DATABASE_URL: str = Field(default="sqlite:///./portfolio.db")
    REDIS_URL: str = Field(default="redis://localhost:6379")

    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ADMIN_PASSWORD: str = Field(default="admin123")

    # Credits Configuration
    DEFAULT_CREDITS: int = Field(default=5)
    EDU_CREDITS: int = Field(default=7)
    COMPANY_CREDITS: int = Field(default=9)

    # Used to build absolute URLs for assets so Gradio doesn't rewrite them
    PUBLIC_BASE_URL: str = "http://localhost:7860"

    # Email Classification
    PERSONAL_EMAIL_DOMAINS: str = Field(
        default="gmail.com,yahoo.com,outlook.com,hotmail.com,icloud.com,protonmail.com,aol.com,mail.com,zoho.com,yandex.com,live.com,msn.com"
    )
    EDU_EMAIL_PATTERNS: str = Field(
        default=".edu,.ac.uk,.edu.au,.edu.in,.ac.in")

    # AI Models
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2")
    LLM_MODEL: str = Field(default="llama-3.3-70b-versatile")

    # RAG Configuration
    CHUNK_SIZE: int = Field(default=800)
    CHUNK_OVERLAP: int = Field(default=100)
    TOP_K_RETRIEVAL: int = Field(default=4)

    # Cache Configuration
    CACHE_SIMILARITY_THRESHOLD: float = Field(default=0.88)
    CACHE_TTL: int = Field(default=86400 * 30)  # 30 days in seconds

    # Rate Limiting
    MAX_CONVERSATION_LENGTH: int = Field(default=20)

    # Paths
    KNOWLEDGE_BASE_PATH: str = Field(default="data/knowledge_base")
    DOCUMENTS_PATH: str = Field(default="data/documents")
    CACHE_PATH: str = Field(default="data/cache")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def personal_domains_list(self) -> List[str]:
        """Return personal email domains as a list."""
        return [d.strip() for d in self.PERSONAL_EMAIL_DOMAINS.split(",")]

    @property
    def edu_patterns_list(self) -> List[str]:
        """Return educational email patterns as a list."""
        return [p.strip() for p in self.EDU_EMAIL_PATTERNS.split(",")]


# Global settings instance
settings = Settings()
