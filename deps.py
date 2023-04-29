from settings import Settings
from db.client import DBClient


def get_db_client() -> DBClient:
    db_client = DBClient()
    return db_client


def get_settings() -> Settings:
    settings = Settings.get_settings()
    return settings
