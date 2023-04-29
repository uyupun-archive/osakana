from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Osakana"
    DESCRIPTION: str = "自動タグ付け機能と検索機能を持つ「あとで読む」記事を管理できるWebアプリ"

    ADDRESS: str = Field("localhost", env="APP_ADDRESS")
    PORT: int = Field("8000", env="APP_PORT")

    class Config:
        env_file: str = ".env"

    def __init__(self, *args, **kwargs):
        load_dotenv()
        super().__init__(*args, **kwargs)

    @classmethod
    @lru_cache
    def get_settings(cls):
        return Settings()
