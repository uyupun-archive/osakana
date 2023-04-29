from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Osakana"
    DESCRIPTION: str = "自動タグ付け機能と検索機能を持つ「あとで読む」記事を管理できるWebアプリ"

    @classmethod
    @lru_cache
    def get_settings(cls):
        return Settings()
