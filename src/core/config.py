from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent.parent


class AppSettings(BaseSettings):
    APP_TITLE: str = "CryptoAPI"
    APP_VERSION: str = "1"

    IS_DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DBSettings(AppSettings):
    SQLITE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    POSTGRES_DB: str = "POSTGRES_DB"
    POSTGRES_USER: str = "POSTGRES_USER"
    POSTGRES_PASSWORD: str = "POSTGRES_PASSWORD"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    def get_pg_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self,
            "DB_URL",
            self.SQLITE_URL if self.IS_DEBUG else self.get_pg_url(),
        )


class CryptoSettings(AppSettings):
    URL: str
    INTERVAL: int = 60


class RedisSettings(AppSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CONNECTION_POOL_MAXSIZE: int = 10
    EXPIRE: int = 3600

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self, "REDIS_HOST", "localhost" if self.IS_DEBUG else "redis"
        )
        object.__setattr__(
            self,
            "REDIS_URL",
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}",
        )


class TaskiqSettings(AppSettings):
    TASKIQ_RETRY_COUNT: int = 5
    TASKIQ_RETRY_DELAY: float | int = 10


class Settings(AppSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    crypto: CryptoSettings = CryptoSettings()
    redis: RedisSettings = RedisSettings()
    taskiq: TaskiqSettings = TaskiqSettings()


settings = Settings()
