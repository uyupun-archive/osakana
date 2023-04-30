from abc import ABC, abstractclassmethod

from db.client import DBClient


class BaseRepository(ABC):
    def __init__(self, db_client: DBClient = DBClient()) -> None:
        self._db_client = db_client

    @abstractclassmethod
    def get_repository(cls):
        pass
