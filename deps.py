from settings import Settings
from db.client import DBClient


def get_db_client():
    db_client = DBClient()
    return db_client


def get_settings():
    settings = Settings.get_settings()
    return settings
