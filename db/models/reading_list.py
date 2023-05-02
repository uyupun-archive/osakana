from __future__ import annotations
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel, HttpUrl

from timezone import get_timezone


class ReadingListRecord(BaseModel):
    id: str | None = None
    url: HttpUrl
    title: str
    is_read: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def set_timestamps(self, timezone: ZoneInfo=get_timezone()) -> None:
        self.created_at = datetime.now(tz=timezone)
        self.updated_at = datetime.now(tz=timezone)

    @classmethod
    def convert_dict(cls, reading_list_record: ReadingListRecord) -> dict[str, Any]:
        document = reading_list_record.dict()
        return document

    @classmethod
    def convert_instance(cls, document: dict[str, Any], timezone: ZoneInfo=get_timezone()) -> ReadingListRecord:
        reading_list_record = ReadingListRecord(
            id=str(document["_id"]),
            url=document["url"],
            title=document["title"],
            is_read=document["is_read"],
            created_at=document["created_at"].astimezone(tz=timezone),
            updated_at=document["updated_at"].astimezone(tz=timezone)
        )
        return reading_list_record
