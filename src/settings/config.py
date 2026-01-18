from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


class Database(Base):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int


class Api(Base):
    BASE_URL: str
    BTC: str
    ETH: str


class Settings(Base):
    database: Database = Database()
    api: Api = Api()


settings = Settings()
