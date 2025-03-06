from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"

    # General
    ORIGINS: list = ["*"]
    # Database
    DB_ENGINE: str = ''
    DB_HOST: str = ''
    DB_USERNAME: str = ''
    DB_PASSWORD: str = ''
    DB_NAME: str = ''
    CELERY_DLQ_EXCHANGE: str = 'default'
    CELERY_DLQ_ROUTING_KEY: str = 'dead-letter'
    CELERY_DLQ_QUEUE: str = 'dead-queue'
    CELERY_DEFAULT_EXCHANGE: str = 'default'
    CELERY_DEFAULT_QUEUE: str = 'default'
    CELERY_DEFAULT_ROUTING_KEY: str = 'default'
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_RETRIES_TIME: int = 3

    BROKER_USER: str = "fapi_admin"
    BROKER_PASSWORD: str = "X7bT9pLqZ2Nf"
    BROKER_HOST: str = "localhost:5672"

    @computed_field  # type: ignore[misc]
    @property
    def broker_url(self) -> str:
        return f"amqp://{self.BROKER_USER}:{self.BROKER_PASSWORD}@{self.BROKER_HOST}"

    @computed_field  # type: ignore[misc]
    @property
    def db_url(self) -> str:
        return f"{self.DB_ENGINE}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:5432/{self.DB_NAME}"

    # Jwt
    JWT_ACCESS_ALGORITHM: str = 'HS256'
    JWT_ACCESS_SECRET_KEY: str = '1'
    JWT_ACCESS_TOKEN_EXPIRED: int = 30  # Minutes

    JWT_REFRESH_ALGORITHM: str = 'HS256'
    JWT_REFRESH_SECRET_KEY: str = '1'
    JWT_REFRESH_TOKEN_EXPIRED: int = 24  # Hours

    # Loader
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings: Settings = Settings()
