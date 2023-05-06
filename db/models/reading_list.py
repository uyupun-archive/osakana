from __future__ import annotations
from datetime import datetime
from uuid import uuid4, UUID
from zoneinfo import ZoneInfo

from pydantic import HttpUrl

from db.client import Document
from db.models.base import OsakanaBaseModel
from lib.timezone import get_timezone


class ReadingListRecord(OsakanaBaseModel):
    id: UUID = uuid4()
    url: HttpUrl
    title: str
    is_read: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    read_at: datetime | None = None

    @classmethod
    def get_name(cls) -> str:
        return "reading_list"

    def set_timestamps(self, timezone: ZoneInfo=get_timezone()) -> None:
        self.created_at = datetime.now(tz=timezone)
        self.updated_at = datetime.now(tz=timezone)

    def update_timestamp(self, timezone: ZoneInfo=get_timezone()) -> None:
        self.updated_at = datetime.now(tz=timezone)

    def read(self, timezone: ZoneInfo=get_timezone()):
        self.is_read = True
        self.read_at = datetime.now(tz=timezone)

    @classmethod
    def convert_dict(cls, reading_list_record: ReadingListRecord) -> Document:
        document = {
            "id": str(reading_list_record.id),
            "url": reading_list_record.url,
            "title": reading_list_record.title,
            "is_read": reading_list_record.is_read,
            "created_at": reading_list_record.created_at.isoformat(),
            "updated_at": reading_list_record.updated_at.isoformat(),
            "read_at": reading_list_record.read_at.isoformat() if reading_list_record.read_at else None
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
            updated_at=document["updated_at"],
            read_at=document["read_at"]
        )
        return reading_list_record
