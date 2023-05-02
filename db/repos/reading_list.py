from __future__ import annotations

from db.models.reading_list import ReadingListRecord
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    def add(self, reading_list_record: ReadingListRecord) -> ReadingListRecord:
        reading_list_record.set_timestamps()
        new_document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        new_document.pop("id")
        created_document = self._db_client.create(
            collection_name="reading_list",
            document=new_document
        )
        created_reading_list_record = ReadingListRecord.convert_instance(document=created_document)
        return created_reading_list_record

    def search(self, keyword: str) -> list[ReadingListRecord]:
        documents = self._db_client.find(
            collection_name="reading_list",
            keyword=keyword
        )
        reading_list = [ReadingListRecord.convert_instance(document=document) for document in documents]
        return reading_list

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
