from pymongo import MongoClient

from db.settings import Settings


class DBClient():
    def __init__(self) -> None:
        settings = Settings.get_settings()
        address = settings.ADDRESS
        port = settings.PORT
        username = settings.USERNAME
        password = settings.PASSWORD

        self._uri = f"mongodb://{username}:{password}@{address}:{port}/"
        self._client = None

    def get_client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(self._uri)
        return self._client
