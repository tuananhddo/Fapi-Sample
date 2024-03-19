import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Any, ClassVar


class Settings(BaseSettings):
    # def __init__(self, **values: Any) -> None:

    #     super().__init__(**values)
    app_name: str = "Awesome API"
    db_engine: str
    db_host: str
    db_username: str
    db_password: str
    db_name: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')



settings = Settings()