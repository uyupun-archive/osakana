from pymongo import MongoClient

from db.settings import get_settings


class DBClient():
    def __init__(self):
        settings = get_settings()
        address = settings.ADDRESS
        port = settings.PORT
        username = settings.USERNAME
        password = settings.PASSWORD

        self._uri = f"mongodb://{username}:{password}@{address}:{port}/"
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = MongoClient(self._uri)
        return self._client
