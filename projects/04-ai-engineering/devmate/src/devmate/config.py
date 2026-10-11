"""
Configuration management for DevMate.
"""

from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _to_asyncpg_url(url: str) -> str:
    """Force the async driver onto a managed Postgres URL.

    Hosting platforms (Render, Heroku) hand out ``postgres://`` or
    ``postgresql://`` connection strings; the app's engine is asyncpg, so the
    scheme must be ``postgresql+asyncpg://``. Idempotent when already async.
    """
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    app_name: str = "devmate"
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="DEBUG")

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # LLM Providers
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.1-8b-instant", alias="GROQ_MODEL")
    default_llm_provider: str = Field(default="ollama", alias="DEFAULT_LLM_PROVIDER")
    default_model: str = Field(default="claude-3-5-sonnet-20241022", alias="DEFAULT_MODEL")
    max_tokens: int = 4096
    temperature: float = 0.1

    # Ollama (local, offline)
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="qwen2.5-coder:7b", alias="OLLAMA_MODEL")
    ollama_embedding_model: str = Field(default="nomic-embed-text", alias="OLLAMA_EMBEDDING_MODEL")

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None
    qdrant_https: bool = Field(default=False, alias="QDRANT_HTTPS")
    qdrant_collection: str = "devmate_code"
    qdrant_vector_size: int = Field(default=768, alias="QDRANT_VECTOR_SIZE")
    qdrant_distance: str = "cosine"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    redis_url: str | None = None

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "devmate"
    postgres_user: str = "devmate"
    postgres_password: str = "devmate"
    database_url: str | None = None

    # Observability
    langfuse_host: str = "http://localhost:3000"
    langfuse_public_key: str | None = Field(default=None, alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str | None = Field(default=None, alias="LANGFUSE_SECRET_KEY")
    tracing_enabled: bool = True
    cost_tracking_enabled: bool = True

    # Auth
    secret_key: str = Field(default="dev-secret-change-in-production", alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    # MCP
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8001

    # Embeddings — offline-first (Ollama); set EMBEDDING_PROVIDER=openai for cloud
    embedding_provider: str = Field(default="ollama", alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")
    embedding_dimensions: int = Field(default=768, alias="EMBEDDING_DIMENSIONS")
    embedding_batch_size: int = 100
    # Point the OpenAI-compatible embeddings client at any provider (Jina,
    # Google, Together, Voyage, ...) to avoid an OpenAI key. Unset = OpenAI.
    embedding_base_url: str | None = Field(default=None, alias="EMBEDDING_BASE_URL")
    embedding_api_key: str | None = Field(default=None, alias="EMBEDDING_API_KEY")

    # RAG
    rag_top_k: int = 20
    rag_rerank_top_k: int = 5
    rag_chunk_size: int = 512
    rag_chunk_overlap: int = 50
    # Retrieved context is part of the prompt budget: 20 x 512-char chunks
    # overflowed qwen2.5-coder:7b's default Ollama context (HTTP 500).
    rag_context_char_budget: int = 8000

    # Demo corpus: a small baked-in dataset ingested on startup when the vector
    # store is empty, so a fresh deploy can answer questions immediately.
    sample_corpus_path: str = Field(default="sample_corpus", alias="SAMPLE_CORPUS_PATH")
    sample_corpus_on_startup: bool = Field(default=True, alias="SAMPLE_CORPUS_ON_STARTUP")

    # Ollama — num_ctx must cover system prompt (with context) + history + answer
    ollama_num_ctx: int = 8192

    # Cache
    cache_ttl_seconds: int = 3600
    semantic_cache_threshold: float = 0.85

    # Guardrails
    max_prompt_length: int = 100000
    pii_detection_enabled: bool = True
    injection_detection_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def _reject_default_secret_in_production(self) -> "Settings":
        """Fail startup when production would sign with the public default key."""
        if self.app_env == "production" and self.secret_key == "dev-secret-change-in-production":
            raise ValueError("SECRET_KEY must be set when APP_ENV=production")
        return self

    @property
    def redis_connection_url(self) -> str:
        if self.redis_url:
            return self.redis_url
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def postgres_connection_url(self) -> str:
        if self.database_url:
            return _to_asyncpg_url(self.database_url)
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
