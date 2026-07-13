from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================
    # Application
    # ==========================
    app_name: str
    app_version: str
    debug: bool

    host: str
    port: int

    secret_key: str

    # ==========================
    # Database
    # ==========================
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()