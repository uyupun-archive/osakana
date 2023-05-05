from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel, HttpUrl

from db.client import Document
from lib.timezone import get_timezone


class ReadingListRecord(BaseModel):
    id: str = str(uuid4())
    url: HttpUrl
    title: str
    is_read: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def get_name(cls) -> str:
        return "reading_list"

    @classmethod
    def has_field(cls, field: str) -> str:
        fields = list(cls.__fields__.keys())
        if field in fields:
            return field
        raise FieldNotFoundError

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


class FieldNotFoundError(Exception):
    pass
