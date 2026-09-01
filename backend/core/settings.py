from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    app_name: str = (
        "Solana Intelligence Platform V3"
    )

    version: str = "3.0.0"

    database_url: str = (
        "sqlite+aiosqlite:///./app.db"
    )

    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()