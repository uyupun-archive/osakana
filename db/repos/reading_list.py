from __future__ import annotations

from db.models.reading_list import ReadingList
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    def add(self, reading_list: ReadingList) -> None:
        inserted_id = self._db_client.add(collection_name="reading_list", document=reading_list.dict())
        print(inserted_id)

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()
