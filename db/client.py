from typing import Any

import pymongo
from pymongo import errors
from pymongo import MongoClient
from pymongo.collection import Collection

from db.settings import Settings


class DBClient:
    def __init__(self, settings: Settings=Settings.get_settings()) -> None:
        address = settings.ADDRESS
        port = settings.PORT
        username = settings.USERNAME
        password = settings.PASSWORD

        self._uri = f"mongodb://{username}:{password}@{address}:{port}/"
        self._db_name = settings.DB_NAME
        self._client = MongoClient(self._uri)

    def _get_collection(self, collection_name: str) -> Collection:
        collection = self._client[self._db_name][collection_name]
        return collection

    def create_unique_constraints(
        self,
        collection_name: str,
        field_names: list[str],
        index_name: str
    ) -> None:
        collection = self._get_collection(collection_name)
        collection.create_index(
            [(field_name, pymongo.ASCENDING) for field_name in field_names],
            name=index_name,
            unique=True
        )

    def create_search_index(
        self,
        collection_name: str,
        field_names: list[str],
        index_name: str
    ) -> None:
        collection = self._get_collection(collection_name)
        collection.create_index(
            [(field_name, pymongo.TEXT) for field_name in field_names],
            name=index_name
        )

    def create(self, collection_name: str, document: dict[str, Any]) -> dict[str, Any]:
        collection = self._get_collection(collection_name)

        try:
            inserted_id = collection.insert_one(document).inserted_id
        except errors.DuplicateKeyError:
            raise URLAlreadyExistsError

        new_document = collection.find_one({"_id": inserted_id})
        if new_document is None:
            raise DocumentNotFoundError
        return new_document

    def find(self, collection_name: str, keyword: str) -> list[dict[str, Any]]:
        collection = self._get_collection(collection_name)
        documents = list(collection.find({"$text": {"$search": keyword}}))
        return documents

    def drop(self, collection_name: str) -> None:
        collection = self._get_collection(collection_name)
        collection.drop()


class DocumentNotFoundError(Exception):
    pass


class URLAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "URL already exists"
