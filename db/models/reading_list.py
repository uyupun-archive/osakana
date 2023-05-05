from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel, HttpUrl

from db.client import Document
from lib.timezone import get_timezone


class ReadingListRecord(BaseModel):
    id: str | None = None
    url: HttpUrl
    title: str
    is_read: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def set_id(self) -> None:
        self.id = str(uuid4())

    def set_timestamps(self, timezone: ZoneInfo=get_timezone()) -> None:
        self.created_at = datetime.now(tz=timezone)
        self.updated_at = datetime.now(tz=timezone)

    @classmethod
    def convert_dict(cls, reading_list_record: ReadingListRecord) -> Document:
        document = {
            "id": reading_list_record.id,
            "url": reading_list_record.url,
            "title": reading_list_record.title,
            "is_read": reading_list_record.is_read,
            "created_at": reading_list_record.created_at.isoformat(),
            "updated_at": reading_list_record.updated_at.isoformat()
        }
        return document

    @classmethod
    def convert_instance(cls, document: Document) -> ReadingListRecord:
        reading_list_record = ReadingListRecord(
            id=document["id"],
            url=document["url"],
            title=document["title"],
            is_read=document["is_read"],
            created_at=document["created_at"],
            updated_at=document["updated_at"]
        )
        return reading_list_record
