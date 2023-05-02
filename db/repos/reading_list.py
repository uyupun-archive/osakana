from __future__ import annotations

from db.models.reading_list import ReadingListRecord, ReadingListIndex
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    def add(self, reading_list_record: ReadingListRecord) -> ReadingListRecord:
        reading_list_record.set_timestamps()
        new_document = {k: v for k, v in reading_list_record.dict().items() if k != "id"}
        created_document = self._db_client.create(
            collection_name="reading_list",
            document=new_document
        )
        created_reading_list_record = ReadingListRecord(
            id=str(created_document["_id"]),
            url=created_document["url"],
            title=created_document["title"],
            is_read=created_document["is_read"],
            created_at=created_document["created_at"],
            updated_at=created_document["updated_at"]
        )
        return created_reading_list_record

    def search(self, keyword: str) -> list[ReadingListRecord]:
        documents = self._db_client.find(
            collection_name="reading_list",
            keyword=keyword,
            index=ReadingListIndex
        )
        reading_list = []
        for document in documents:
            reading_list.append(ReadingListRecord(
                id=str(document["_id"]),
                url=document["url"],
                title=document["title"],
                is_read=document["is_read"],
                created_at=document["created_at"],
                updated_at=document["updated_at"]
            ))
        return reading_list

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
