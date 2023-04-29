from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    ADDRESS: str
    PORT: int
    USERNAME: str
    PASSWORD: str

    class Config:
        env_file: str = ".env"


@lru_cache
def get_settings():
    return Settings()
