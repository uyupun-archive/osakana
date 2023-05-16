from __future__ import annotations
import random
from uuid import UUID

from db.client import Document, DocumentNotFoundError, DocumentAlreadyExistsError
from db.models.reading_list import ReadingListRecord
from db.repos.base import BaseRepository


class ReadingListRepository(BaseRepository):
    _index_name = "reading_list"

    def add(self, reading_list_record: ReadingListRecord) -> None:
        document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        try:
            self._db_client.add_document(
                index_name=self._index_name,
                key="url",
                document=document
            )
        except DocumentAlreadyExistsError:
            raise UrlAlreadyExistsError()

    def find(self, id: UUID) -> ReadingListRecord:
        document = self._db_client.get_document(
            index_name=self._index_name,
            id=id
        )
        reading_list_record = ReadingListRecord.convert_instance(document=document)
        return reading_list_record

    def search(self, keyword: str) -> list[ReadingListRecord]:
        documents = self._db_client.search_documents(
            index_name=self._index_name,
            keyword=keyword,
            options={"sort": ["created_at:desc"]}
        )
        reading_list = [ReadingListRecord.convert_instance(document=document) for document in documents]
        return reading_list

    def random(self) -> ReadingListRecord:
        document_ids = self._get_oldest_document_ids()
        random_id = random.choice(document_ids)
        document = self._get_random_document(random_id=random_id)

        reading_list_record = ReadingListRecord.convert_instance(document=document)
        return reading_list_record

    def _get_oldest_document_ids(self) -> list[str]:
        documents = self._db_client.search_documents(
            index_name=self._index_name,
            options={"attributesToRetrieve": ["id"], "limit": 1000, "sort": ["updated_at:asc"]}
        )
        document_ids = [document["id"] for document in documents]
        return document_ids

    def _get_random_document(self, random_id: str) -> Document:
        document = self._db_client.search_documents(
            index_name=self._index_name,
            keyword=random_id
        )[0]
        return document

    def read(self, id: UUID) -> None:
        try:
            reading_list_record = self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()
        if reading_list_record.is_read:
            raise ReadingListRecordAlreadyReadError()

        reading_list_record.read()
        document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.update_document(
            index_name=self._index_name,
            document=document
        )

    def unread(self, id: UUID) -> None:
        try:
            reading_list_record = self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()
        if not reading_list_record.is_read:
            raise ReadingListRecordNotYetReadError()

        reading_list_record.unread()
        document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.update_document(
            index_name=self._index_name,
            document=document
        )

    def delete(self, id: UUID) -> None:
        try:
            self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()

        self._db_client.delete_document(
            index_name=self._index_name,
            id=id
        )

    def bookmark(self, id: UUID) -> None:
        try:
            reading_list_record = self.find(id=id)
        except DocumentNotFoundError:
            raise ReadingListRecordNotFoundError()

        reading_list_record.bookmark()
        document = ReadingListRecord.convert_dict(reading_list_record=reading_list_record)
        self._db_client.update_document(
            index_name=self._index_name,
            document=document
        )

    @classmethod
    def get_repository(cls) -> ReadingListRepository:
        return cls()


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