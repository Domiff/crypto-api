from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    SQLITE_URL: str = "sqlite+aiosqlite:///./crypto.db"
        
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    BASE_URL: str
    BTC: str
    ETH: str

    CELERY_BROKER_URL: str

    IS_DEBUG: bool = False
    IS_DOCKERIZED: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    def get_pg_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self,
            "DB_URL",
            self.get_pg_url() if self.IS_DOCKERIZED else self.SQLITE_URL,
        )


settings = Settings()
