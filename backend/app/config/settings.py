"""Configuration settings management."""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = False
    app_log_level: str = "INFO"
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/incidentiq"
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_db: int = 0
    redis_timeout: int = 30
    
    # Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.7
    gemini_max_output_tokens: int = 4096
    gemini_timeout: int = 60
    
    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_batch_size: int = 32
    embedding_device: str = "cpu"
    
    # Reranking Model
    reranking_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    reranking_top_k: int = 5
    reranking_batch_size: int = 32
    
    # RAG Configuration
    chunk_size: int = 512
    chunk_overlap: int = 128
    retrieval_top_k: int = 10
    retrieval_score_threshold: float = 0.5
    
    # Agent Configuration
    max_investigation_steps: int = 20
    max_tool_retries: int = 3
    investigation_timeout_seconds: int = 300
    
    # Evaluation Configuration
    evaluation_sample_size: int = 100
    evaluation_batch_size: int = 10
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.app_env == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.app_env == "development"
