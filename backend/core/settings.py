from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    app_name: str = (
        "Solana Intelligence Platform V3"
    )

    version: str = "3.0.0-alpha.1"

    environment: str = "development"

    host: str = "0.0.0.0"

    port: int = 8000

    database_url: str = (
        "sqlite+aiosqlite:///./solana_v3.db"
    )

    log_level: str = "INFO"

    enable_metrics: bool = True

    scheduler_interval_seconds: float = 15.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()