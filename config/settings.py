from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # Gemini API Settings (using OpenAI-compatible endpoint)
    gemini_api_key: Optional[str] = None
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    gemini_model: str = "gemini-2.5-flash"

    # Alternative: OpenAI API (fallback)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"

    # Application settings
    app_name: str = "ERP Intelligence Agent"
    max_file_size_mb: int = 50
    supported_extensions: tuple = (".csv", ".xlsx", ".xls")

    # Analysis settings
    dead_stock_threshold_days: int = 180
    overstock_threshold_days: int = 90
    customer_concentration_warning_pct: float = 20.0
    customer_concentration_critical_pct: float = 30.0

    # Agent settings
    use_gemini: bool = True  # Set to False to use OpenAI
    max_tokens: int = 4000
    temperature: float = 0.1

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
