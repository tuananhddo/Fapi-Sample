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
    jwt_secret_key: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings = Settings()