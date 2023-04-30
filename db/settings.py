from __future__ import annotations
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_NAME: str
    ADDRESS: str = Field("localhost", env="DB_ADDRESS")
    PORT: int = Field(27017, env="DB_PORT")
    USERNAME: str = Field("root", env="DB_USERNAME")
    PASSWORD: str = Field("password", env="DB_PASSWORD")

    class Config:
        env_file: str = ".env"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        load_dotenv()

    @classmethod
    @lru_cache(maxsize=1)
    def get_settings(cls) -> Settings:
        return Settings()
