from typing import Any, Type

import pymongo
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

from db.settings import Settings
from db.models.reading_list import ReadingListIndex


class DBClient:
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
        collection = client[self._db_name][collection_name]
        return collection

    def _create_index(self, collection: Collection, index: Type[BaseModel]) -> None:
        _index = []
        for name, field in index.__fields__.items():
            if issubclass(field.type_, str):
                _index.append((name, pymongo.TEXT))
                continue
            raise IndexTypeNotSupportedError
        collection.create_index(_index)

    def create(self, collection_name: str, document: dict[str, Any]) -> dict[str, Any]:
        collection = self._get_collection(collection_name)
        inserted_id = collection.insert_one(document).inserted_id
        new_document = collection.find_one({"_id": inserted_id})
        if new_document is None:
            raise DocumentNotFoundError
        return new_document

    def find(self, collection_name: str, keyword: str, index: Type[ReadingListIndex]) -> list[dict[str, Any]]:
        collection = self._get_collection(collection_name)
        self._create_index(collection=collection, index=index)
        documents = list(collection.find({"$text": {"$search": keyword}}))
        return documents


class IndexTypeNotSupportedError(Exception):
    pass


class DocumentNotFoundError(Exception):
    pass
