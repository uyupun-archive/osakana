from __future__ import annotations

import random
from enum import Enum
from uuid import UUID

from db.client import DocumentAlreadyExistsError, DocumentNotFoundError, Options
from db.models.reading_list import PrivateReadingListRecord, ReadingListRecord
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    _index_name = "reading_list"

    def add(self, reading_list_record: ReadingListRecord) -> None:
        reading_list_record.set_title_ngrams()
        reading_list_record.set_title_morphemes()
        document = ReadingListRecord.convert_dict(
            reading_list_record=reading_list_record
        )
        try:
            self._db_client.add_document(
                index_name=self._index_name, key="url", document=document
            )
        except DocumentAlreadyExistsError:
            raise UrlAlreadyExistsError()

    def find(self, id: UUID) -> ReadingListRecord:
        document = self._db_client.get_document(index_name=self._index_name, id=id)
        reading_list_record = ReadingListRecord.convert_instance(document=document)
        return reading_list_record

    def search(
        self,
        keyword: str,
        is_bookmarked: bool = False,
        is_read: bool = False,
        is_unread: bool = False,
    ) -> list[ReadingListRecord]:
        filters = self._create_filters(
            is_bookmarked=is_bookmarked, is_read=is_read, is_unread=is_unread
        )
        options = {"sort": ["created_at:desc"], "filter": filters}

        documents = self._db_client.search_documents(
            index_name=self._index_name,
            keyword=keyword,
            options=options,
        )
        reading_list = [
            ReadingListRecord.convert_instance(document=document)
            for document in documents
        ]
        return reading_list

    def _create_filters(
        self, is_bookmarked: bool, is_read: bool, is_unread: bool
    ) -> str:
        filters = []

        if is_bookmarked:
            filters.append("is_bookmarked = true")
        if is_read:
            filters.append("is_read = true")
        if is_unread:
            filters.append("is_read = false")

        return " AND ".join(filters)

    def random(self) -> ReadingListRecord:
        document_ids = self._get_document_ids()
        reading_list_record = self._get_random_record(document_ids=document_ids)
        return reading_list_record

    def _get_document_ids(self) -> list[UUID]:
        documents = self._db_client.search_documents(
            index_name=self._index_name,
            options={
                "attributesToRetrieve": ["id"],
                "limit": 1000,
                "sort": ["updated_at:asc"],
            },
        )
        document_ids = [document["id"] for document in documents]
        return document_ids

    def _get_random_record(self, document_ids: list[UUID]) -> ReadingListRecord:
        random_id = random.choice(document_ids)
        try:
            reading_list_record = self.find(id=random_id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()
        return reading_list_record

    def read(self, id: UUID) -> None:
        try:
            reading_list_record = self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()
        if reading_list_record.is_read:
            raise ReadingListRecordAlreadyReadError()

        reading_list_record.read()
        document = ReadingListRecord.convert_dict(
            reading_list_record=reading_list_record
        )
        self._db_client.update_document(index_name=self._index_name, document=document)

    def unread(self, id: UUID) -> None:
        try:
            reading_list_record = self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()
        if not reading_list_record.is_read:
            raise ReadingListRecordNotYetReadError()

        reading_list_record.unread()
        document = ReadingListRecord.convert_dict(
            reading_list_record=reading_list_record
        )
        self._db_client.update_document(index_name=self._index_name, document=document)

    def delete(self, id: UUID) -> None:
        try:
            self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()

        self._db_client.delete_document(index_name=self._index_name, id=id)

    def bookmark(self, id: UUID) -> None:
        try:
            reading_list_record = self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()

        reading_list_record.bookmark()
        document = ReadingListRecord.convert_dict(
            reading_list_record=reading_list_record
        )
        self._db_client.update_document(index_name=self._index_name, document=document)

    def count(self, type: ReadingListCountType) -> int:
        options: Options = {}
        if type != ReadingListCountType.IS_ALL:
            options = {"filter": type.value}

        count = self._db_client.count_documents(
            index_name=self._index_name, options=options
        )
        return count

    def all(self) -> list[PrivateReadingListRecord]:
        options: Options = {"sort": ["created_at:asc"]}
        documents = self._db_client.search_documents(
            index_name=self._index_name,
            keyword="",
            options=options,
        )
        reading_list = [
            PrivateReadingListRecord.convert_instance(document=document)
            for document in documents
        ]
        return reading_list

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()


class ReadingListCountType(Enum):
    IS_ALL = ""
    IS_READ = "is_read = true"
    IS_UNREAD = "is_read = false"
    IS_BOOKMARKED = "is_bookmarked = true"


class UrlAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "URL already exists"


class ReadingListRecordNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "Reading list record not found"


class ReadingListRecordAlreadyReadError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "Reading list record already read"


class ReadingListRecordNotYetReadError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "Reading list record already unread"
