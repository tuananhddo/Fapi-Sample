import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Any, ClassVar


class Settings(BaseSettings):
    app_name: str = "Awesome API"

    #General
    origins: list = ["*"]
    #Database
    db_engine: str
    db_host: str
    db_username: str
    db_password: str
    db_name: str
    #Jwt
    jwt_access_algorithm: str
    jwt_access_secret_key: str
    jwt_access_token_expired: int = 30 # Minutes

    jwt_refresh_algorithm: str
    jwt_refresh_secret_key: str
    jwt_refresh_token_expired: int = 24 # Hours

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings: Settings = Settings()