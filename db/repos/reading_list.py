from __future__ import annotations

from db.models.reading_list import ReadingListRecord
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    _collection_name = "reading_list"

    def add(self, reading_list_record: ReadingListRecord) -> None:
        reading_list_record.set_id()
        reading_list_record.set_timestamps()
        new_document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.add_document(
            index_name=self._collection_name,
            document=new_document
        )

    def search(self, keyword: str) -> list[ReadingListRecord]:
        documents = self._db_client.search_documents(
            index_name=self._collection_name,
            keyword=keyword
        )
        reading_list = [ReadingListRecord.convert_instance(document=document) for document in documents]
        return reading_list

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
