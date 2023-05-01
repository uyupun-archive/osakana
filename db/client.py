from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pymongo import MongoClient
from pymongo.collection import Collection

from db.settings import Settings
from timezone import get_timezone


class DBClient():
    def __init__(self, settings: Settings=Settings.get_settings()) -> None:
        address = settings.ADDRESS
        port = settings.PORT
        username = settings.USERNAME
        password = settings.PASSWORD

        self._uri = f"mongodb://{username}:{password}@{address}:{port}/"
        self._db_name = settings.DB_NAME
        self._client = None

    def _get_client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(self._uri)
        return self._client

    def _get_collection(self, collection_name: str) -> Collection:
        client = self._get_client()
        return client[self._db_name][collection_name]

    def add(
        self,
        collection_name: str,
        document: dict[str, Any],
        timezone: ZoneInfo=get_timezone()
    ) -> str:
        collection = self._get_collection(collection_name)
        document["created_at"] = datetime.now(tz=timezone)
        document["updated_at"] = datetime.now(tz=timezone)
        res = collection.insert_one(document)
        return str(res.inserted_id)
