"""
Application configuration loaded from environment variables.

Why Pydantic Settings? It validates types at startup — if DATABASE_URL is missing,
the app crashes immediately with a clear error instead of failing on the first
database query 10 minutes into a debugging session.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str

    # Redis
    redis_url: str

    # Auth
    clerk_secret_key: str = ""
    clerk_jwks_url: str = "https://api.clerk.com/.well-known/jwks.json"

    # Internal
    internal_worker_secret: str = "change-me"

    # LLM Providers
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    cohere_api_key: str = ""
    mistral_api_key: str = ""
    groq_api_key: str = ""

    # Langfuse
    langfuse_secret_key: str = ""
    langfuse_public_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_service_role_key: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]