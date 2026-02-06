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


# from app.utils import TEMPLATES_DIR
class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_FROM: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str

    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    VALIDATE_CERTS: bool = True
    USE_CREDENTIALS: bool = True
    # TEMPLATE_FOLDER: str = f"{TEMPLATES_DIR}"

    model_config = _base_config


database_settings = Databasesettings()
token_settings = TokenSettings()
notification_settings = NotificationSettings()
# print(settings.POSTGRES_DB)
# print(settings.POSTGRES_PORT)
