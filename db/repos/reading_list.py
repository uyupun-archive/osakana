from __future__ import annotations

from db.models.reading_list import ReadingListRecord, ReadingListIndex
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    def add(self, reading_list_record: ReadingListRecord) -> str:
        inserted_id = self._db_client.add(
            collection_name="reading_list",
            document=reading_list_record.dict()
        )
        return inserted_id

    def search(self, keyword: str) -> list[dict]:
        reading_list = self._db_client.search(
            collection_name="reading_list",
            keyword=keyword,
            index=ReadingListIndex
        )
        return reading_list

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
