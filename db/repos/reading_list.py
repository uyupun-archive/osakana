from __future__ import annotations
import random
from uuid import UUID

from db.client import Document
from db.models.reading_list import ReadingListRecord
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    _index_name = "reading_list"

    def add(self, reading_list_record: ReadingListRecord) -> None:
        reading_list_record.set_timestamps()
        document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.add_document(
            index_name=self._index_name,
            key="url",
            document=document
        )

    def find(self, id: UUID) -> ReadingListRecord:
        document = self._db_client.get_document(
            index_name=self._index_name,
            id=id
        )
        reading_list = ReadingListRecord.convert_instance(document=document)
        return reading_list

    def search(self, keyword: str) -> list[ReadingListRecord]:
        documents = self._db_client.search_documents(
            index_name=self._index_name,
            keyword=keyword
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
            index_name=self._index_name,
            options={"attributesToRetrieve": ["id"], "limit": 1000, "sort": ["updated_at:asc"]}
        )
        document_ids = [document["id"] for document in documents]
        return document_ids

    def _get_random_document(self, random_id: str) -> Document:
        document = self._db_client.search_documents(
            index_name=self._index_name,
            keyword=random_id
        )[0]
        return document

    def read(self, reading_list_record: ReadingListRecord) -> None:
        reading_list_record.update_timestamp()
        reading_list_record.read()
        document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.update_document(
            index_name=self._index_name,
            document=document
        )

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
