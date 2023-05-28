from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from pydantic import Field, HttpUrl, PrivateAttr

from db.client import Document
from db.models.base import OsakanaBaseModel
from services.morphological_analysis import MorphologicalAnalysisService
from services.ngrams import NgramService
from services.timezone import get_timezone


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
    _title_morphemes: list[str] = PrivateAttr(default=[])

    @classmethod
    def get_name(cls) -> str:
        return "reading_list"

    def set_title_ngrams(self, service: NgramService = NgramService()):
        self._title_bigrams = service.generate(text=self.title, n=2)
        self._title_trigrams = service.generate(text=self.title, n=3)

    def set_title_morphemes(
        self, service: MorphologicalAnalysisService = MorphologicalAnalysisService()
    ):
        self._title_morphemes = service.generate(text=self.title)

    def _update_timestamp(self, timezone: ZoneInfo = get_timezone()) -> None:
        self.updated_at = datetime.now(tz=timezone)

    def read(self, timezone: ZoneInfo = get_timezone()):
        self._update_timestamp()
        self.is_read = True
        self.read_at = datetime.now(tz=timezone)

    def unread(self):
        self._update_timestamp()
        self.is_read = False
        self.read_at = None

    def bookmark(self, timezone: ZoneInfo = get_timezone()):
        self._update_timestamp()
        self.is_bookmarked = not self.is_bookmarked
        if self.is_bookmarked:
            self.bookmarked_at = datetime.now(tz=timezone)
        else:
            self.bookmarked_at = None

    @classmethod
    def convert_dict(cls, reading_list_record: ReadingListRecord) -> Document:
        document = reading_list_record.dict()

        document["id"] = str(reading_list_record.id)
        document["_title_bigrams"] = reading_list_record._title_bigrams
        document["_title_trigrams"] = reading_list_record._title_trigrams
        document["_title_morphemes"] = reading_list_record._title_morphemes
        document["created_at"] = reading_list_record.created_at.isoformat()
        document["updated_at"] = reading_list_record.updated_at.isoformat()

        if reading_list_record.read_at:
            document["read_at"] = reading_list_record.read_at.isoformat()
        if reading_list_record.bookmarked_at:
            document["bookmarked_at"] = reading_list_record.bookmarked_at.isoformat()

        return document

    @classmethod
    def convert_instance(cls, document: Document) -> ReadingListRecord:
        return ReadingListRecord(**document)


class PrivateReadingListRecord(ReadingListRecord):
    title_bigrams: list[str] = Field(default=[])
    title_trigrams: list[str] = Field(default=[])
    title_morphemes: list[str] = Field(default=[])

    @classmethod
    def convert_dict(
        cls, private_reading_list_record: PrivateReadingListRecord
    ) -> Document:
        document = ReadingListRecord.convert_dict(private_reading_list_record)
        return document

    @classmethod
    def convert_instance(cls, document: Document) -> PrivateReadingListRecord:
        return PrivateReadingListRecord(
            **document,
            title_bigrams=document["_title_bigrams"],
            title_trigrams=document["_title_trigrams"],
            title_morphemes=document["_title_morphemes"],
        )


PrivateReadingList = list[PrivateReadingListRecord]
