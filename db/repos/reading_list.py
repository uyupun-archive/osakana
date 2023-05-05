from __future__ import annotations
import random

from db.models.reading_list import ReadingListRecord
from db.repos.base import BaseRepository

from db.client import Document


class ReadingListRepository(BaseRepository):
    _collection_name = "reading_list"

    def add(self, reading_list_record: ReadingListRecord) -> None:
        reading_list_record.set_timestamps()
        new_document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.add_document(
            index_name=self._collection_name,
            key="url",
            document=new_document
        )

    def search(self, keyword: str) -> list[ReadingListRecord]:
        documents = self._db_client.search_documents(
            index_name=self._collection_name,
            keyword=keyword,
            options={"attributesToHighlight": ["title", "url"]}
        )
        reading_list = [ReadingListRecord.convert_instance(document=document) for document in documents]
        return reading_list

    def random(self) -> ReadingListRecord:
        document_ids = self._get_oldest_document_ids()
        random_id = random.choice(document_ids)
        document = self._get_random_document(random_id=random_id)

        reading_list_record = ReadingListRecord.convert_instance(document=document)
        return reading_list_record

    def _get_oldest_document_ids(self) -> list[str]:
        documents = self._db_client.search_documents(
            index_name=self._collection_name,
            options={"attributesToRetrieve": ["id"], "limit": 1000, "sort": ["updated_at:asc"]}
        )
        document_ids = [document["id"] for document in documents]
        return document_ids

    def _get_random_document(self, random_id: str) -> Document:
        document = self._db_client.search_documents(
            index_name=self._collection_name,
            keyword=random_id,
            options={"attributesToHighlight": ["id"]}
        )[0]
        return document

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
