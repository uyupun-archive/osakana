from settings import Settings
from db.repos.reading_list import ReadingListRepository


def get_global_settings() -> Settings:
    settings = Settings.get_settings()
    return settings


def get_reading_list_repository() -> ReadingListRepository:
    return ReadingListRepository.get_repository()
