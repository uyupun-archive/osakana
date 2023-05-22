from abc import ABC, abstractmethod

from db.client import DBClient


class BaseMigrator(ABC):
    def __init__(self, db_client: DBClient = DBClient()) -> None:
        self._db_client = db_client

    @abstractmethod
    def get_name(self):
        raise NotImplementedError()

    @abstractmethod
    def up(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def down(self) -> None:
        raise NotImplementedError()
