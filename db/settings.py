from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    ADDRESS: str = Field("localhost", env="DB_ADDRESS")
    PORT: int = Field(27017, env="DB_PORT")
    USERNAME: str = Field("root", env="DB_USERNAME")
    PASSWORD: str = Field("password", env="DB_PASSWORD")

    class Config:
        env_file: str = ".env"

    def __init__(self, *args, **kwargs):
        load_dotenv()
        super().__init__(*args, **kwargs)

    @classmethod
    @lru_cache
    def get_settings(cls):
        return Settings()
