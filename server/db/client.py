from enum import Enum
from time import sleep
from typing import Any
from uuid import UUID

import meilisearch
from meilisearch.errors import MeilisearchApiError
from meilisearch.models.task import TaskInfo

from db.settings import Settings

Document = dict[str, Any]


Documents = list[Document]


Options = dict[str, list[str] | str | int]


class DBClient:
    def __init__(self, settings: Settings = Settings.get_settings()) -> None:
        address = settings.ADDRESS
        port = settings.PORT

        self._uri = f"http://{address}:{port}"
        self._client = meilisearch.Client(url=self._uri)

    def create_index(self, index_name: str) -> None:
        self._client.create_index(uid=index_name)

    def delete_index(self, index_name: str) -> None:
        self._client.delete_index(uid=index_name)

    def sortable(self, index_name: str, attributes: list[str]) -> None:
        self._client.index(uid=index_name).update_settings(
            {"sortableAttributes": attributes}
        )

    def filterable(self, index_name: str, attributes: list[str]) -> None:
        self._client.index(uid=index_name).update_settings(
            {"filterableAttributes": attributes}
        )

    def add_document(self, index_name: str, document: Document, key: str) -> None:
        index = self._client.index(uid=index_name)

        documents = self.search_documents(
            index_name=index_name, keyword=f'"{document[key]}"'
        )
        if documents:
            raise DocumentAlreadyExistsError()

        task = index.add_documents(documents=[document])
        self._check_task_status(index_name=index_name, task=task)

    def add_documents(self, index_name: str, documents: Documents) -> None:
        index = self._client.index(uid=index_name)

        duplicate_id = self._are_duplicate_documents(
            index_name=index_name, documents=documents
        )
        if duplicate_id:
            raise DocumentIdDuplicateError(id=duplicate_id)

        task = index.add_documents(documents=documents)
        self._check_task_status(index_name=index_name, task=task)

    def _are_duplicate_documents(
        self, index_name: str, documents: Documents
    ) -> UUID | None:
        existing_documents = self.search_documents(
            index_name=index_name,
            keyword="",
            options={},
        )

        existing_ids = []
        ids = []
        try:
            existing_ids = [document["id"] for document in existing_documents]
            ids = [document["id"] for document in documents]
        except KeyError:
            raise DocumentIdNotFoundError()

        for id in ids:
            if id in existing_ids:
                return id
        return None

    def get_document(self, index_name: str, id: UUID) -> Document:
        try:
            document = self._client.index(uid=index_name).get_document(
                document_id=str(id)
            )
        except MeilisearchApiError as e:
            raise DocumentNotFoundError(e)
        return dict(document)["_Document__doc"]

    def search_documents(
        self, index_name: str, options: Options = {}, keyword: str = ""
    ) -> Documents:
        documents = self._client.index(uid=index_name).search(
            query=keyword, opt_params=options
        )
        return documents["hits"]

    def update_document(self, index_name: str, document: Document) -> None:
        task = self._client.index(uid=index_name).update_documents(documents=[document])
        self._check_task_status(index_name=index_name, task=task)

    def delete_document(self, index_name: str, id: UUID) -> None:
        self.get_document(index_name=index_name, id=id)

        index = self._client.index(uid=index_name)
        task = index.delete_document(document_id=str(id))
        self._check_task_status(index_name=index_name, task=task)

    def count_documents(self, index_name: str, options: Options = {}) -> int:
        documents = self.search_documents(index_name=index_name, options=options)
        count = len(documents)
        return count

    def _check_task_status(self, index_name: str, task: TaskInfo) -> None:
        task_status = None
        while task_status != TaskStatus.Succeeded:
            sleep(1)
            task_status = (
                self._client.index(uid=index_name).get_task(uid=task.task_uid).status
            )

            if task_status == TaskStatus.Failed:
                raise InvalidDocumentError()


class TaskStatus(str, Enum):
    Succeeded = "succeeded"
    Failed = "failed"


class DocumentAlreadyExistsError(Exception):
    pass


class DocumentNotFoundError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass


class DocumentIdDuplicateError(Exception):
    def __init__(self, id: UUID) -> None:
        super().__init__()
        self.id = id


class DocumentIdNotFoundError(Exception):
    pass
