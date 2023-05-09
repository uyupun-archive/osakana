from enum import Enum
from time import sleep
from typing import Any
from uuid import UUID

import meilisearch
from meilisearch.models.task import TaskInfo
from meilisearch.errors import MeilisearchApiError

from db.settings import Settings


Document = dict[str, Any]


Documents = list[Document]


class DBClient:
    def __init__(self, settings: Settings=Settings.get_settings()) -> None:
        address = settings.ADDRESS
        port = settings.PORT

        self._uri = f"http://{address}:{port}"
        self._client = meilisearch.Client(url=self._uri)

    def create_index(self, index_name: str) -> None:
        if self._exists_index(index_name=index_name):
            raise IndexAlreadyExistsError()
        self._client.create_index(uid=index_name)

    def delete_index(self, index_name: str) -> None:
        if not self._exists_index(index_name=index_name):
            raise IndexDoesNotExistsError()
        self._client.delete_index(uid=index_name)

    def _exists_index(self, index_name: str) -> bool:
        indexes = self._client.get_indexes()["results"]
        if index_name in [index.uid for index in indexes]:
            return True
        return False

    def sortable(self, index_name: str, attribute: str) -> None:
        self._client.index(uid=index_name).update_settings({"sortableAttributes": [attribute]})

    def add_document(self, index_name: str, key: str, document: Document) -> None:
        index = self._client.index(uid=index_name)

        documents = self.search_documents(
            index_name=index_name,
            keyword=f'"{document[key]}"'
        )
        if documents:
            raise DocumentAlreadyExistsError()

        task = index.add_documents(documents=[document])
        self._check_task_status(index_name=index_name, task=task)

    def get_document(self, index_name: str, id: UUID) -> Document:
        try:
            document = self._client.index(uid=index_name).get_document(document_id=str(id))
        except MeilisearchApiError as e:
            raise DocumentNotFoundError(e)
        return dict(document)["_Document__doc"]

    def search_documents(self, index_name: str, options: dict={}, keyword: str="") -> Documents:
        documents = self._client.index(uid=index_name).search(query=keyword, opt_params=options)
        return documents["hits"]

    def update_document(self, index_name: str, document: Document) -> None:
        task = self._client.index(uid=index_name).update_documents(documents=[document])
        self._check_task_status(index_name=index_name, task=task)

    def delete_document(self, index_name: str, id: UUID) -> None:
        self.get_document(index_name=index_name, id=id)

        index = self._client.index(uid=index_name)
        task = index.delete_document(document_id=str(id))
        self._check_task_status(index_name=index_name, task=task)

    def _check_task_status(self, index_name: str, task: TaskInfo) -> None:
        task_status = None
        while task_status != TaskStatus.Succeeded:
            sleep(1)
            task_status = self._client.index(uid=index_name).get_task(uid=task.task_uid).status

            if task_status == TaskStatus.Failed:
                raise InvalidDocumentError()


class TaskStatus(str, Enum):
    Succeeded = "succeeded"
    Failed = "failed"


class IndexAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "Index already exists"


class IndexDoesNotExistsError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "Index not exists"


class DocumentAlreadyExistsError(Exception):
    pass


class DocumentNotFoundError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass
