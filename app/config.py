from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime

_base_config = SettingsConfigDict(
    env_file="./.env", env_ignore_empty=True, extra="ignore"
)


class Databasesettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URL: str  # postgresql+asyncpg://username:password@localhost:5432/dbname
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = _base_config


class TokenSettings(BaseSettings):
    HASH_ALGO: str
    SECRET_KEY: str
    EXP_TIME: int

    model_config = _base_config


database_settings = Databasesettings()
token_settings = TokenSettings()
# print(settings.POSTGRES_DB)
# print(settings.POSTGRES_PORT)
