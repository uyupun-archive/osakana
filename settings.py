from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Osakana"
    DESCRIPTION: str = "自動タグ付け機能と検索機能を持つ「あとで読む」記事を管理できるWebアプリ"


@lru_cache
def get_settings():
    return Settings()
