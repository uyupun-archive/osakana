from pymongo import MongoClient


class DBClient():
    def __init__(self):
        username = "root"
        password = "password"
        self._uri = f"mongodb://{username}:{password}@localhost:27017/"
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = MongoClient(self._uri)
        return self._client
