from __future__ import annotations
from datetime import datetime
from uuid import uuid4, UUID
from zoneinfo import ZoneInfo

from pydantic import Field, HttpUrl, PrivateAttr

from db.client import Document
from db.models.base import OsakanaBaseModel
from lib.ngrams import NgramService
from lib.timezone import get_timezone


class ReadingListRecord(OsakanaBaseModel):
    id: UUID = Field(default_factory=uuid4)
    url: HttpUrl
    title: str
    is_read: bool = False
    is_bookmarked: bool = False
    thumb: HttpUrl | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    read_at: datetime | None = None
    bookmarked_at: datetime | None = None

    _title_bigrams: list[str] = PrivateAttr(default=[])
    _title_trigrams: list[str] = PrivateAttr(default=[])

    @classmethod
    def get_name(cls) -> str:
        return "reading_list"

    def set_title_ngrams(self, ngram_service: NgramService = NgramService()):
        self._title_bigrams = ngram_service.generate(text=self.title, n=2)
        self._title_trigrams = ngram_service.generate(text=self.title, n=3)

    def _update_timestamp(self, timezone: ZoneInfo=get_timezone()) -> None:
        self.updated_at = datetime.now(tz=timezone)

    def read(self, timezone: ZoneInfo=get_timezone()):
        self._update_timestamp()
        self.is_read = True
        self.read_at = datetime.now(tz=timezone)

    def unread(self):
        self._update_timestamp()
        self.is_read = False
        self.read_at = None

    def bookmark(self, timezone: ZoneInfo=get_timezone()):
        self._update_timestamp()
        self.is_bookmarked = not self.is_bookmarked
        if self.is_bookmarked:
            self.bookmarked_at = datetime.now(tz=timezone)
        else:
            self.bookmarked_at = None

    @classmethod
    def convert_dict(cls, reading_list_record: ReadingListRecord) -> Document:
        document = {
            "id": str(reading_list_record.id),
            "url": reading_list_record.url,
            "title": reading_list_record.title,
            "_title_bigrams": reading_list_record._title_bigrams,
            "_title_trigrams": reading_list_record._title_trigrams,
            "is_read": reading_list_record.is_read,
            "is_bookmarked": reading_list_record.is_bookmarked,
            "thumb": reading_list_record.thumb,
            "created_at": reading_list_record.created_at.isoformat(),
            "updated_at": reading_list_record.updated_at.isoformat(),
            "read_at": reading_list_record.read_at.isoformat() if reading_list_record.read_at else None,
            "bookmarked_at": reading_list_record.bookmarked_at.isoformat() if reading_list_record.bookmarked_at else None
        }
        return document

    @classmethod
    def convert_instance(cls, document: Document) -> ReadingListRecord:
        reading_list_record = ReadingListRecord(
            id=document["id"],
            url=document["url"],
            title=document["title"],
            is_read=document["is_read"],
            is_bookmarked=document["is_bookmarked"],
            thumb=document["thumb"],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
            read_at=document["read_at"],
            bookmarked_at=document["bookmarked_at"]
        )
        return reading_list_record
