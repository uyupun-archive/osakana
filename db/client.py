from enum import Enum
from time import sleep
from typing import Any

import meilisearch
from meilisearch.models.task import TaskInfo

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
        self._client.create_index(uid=index_name)
        # TODO: すでにインデックスが存在する場合の警告

    def delete_index(self, index_name: str) -> None:
        self._client.delete_index(uid=index_name)
        # TODO: インデックスが存在しない場合の警告

    def add_document(self, index_name: str, document: Document) -> None:
        index = self._client.index(uid=index_name)

        documents = self.search_documents(index_name=index_name, attributes=["url"], keyword=document["url"])
        if documents:
            raise URLAlreadyExistsError

        task = index.add_documents(documents=[document])
        self._check_task_status(index_name=index_name, task=task)

    def _check_task_status(self, index_name: str, task: TaskInfo) -> None:
        task_status = None
        while task_status != TaskStatus.Succeeded:
            sleep(1)
            task_status = self._client.index(uid=index_name).get_task(uid=task.task_uid).status

            if task_status == TaskStatus.Failed:
                raise InvalidDocumentError

    def search_documents(self, index_name: str, attributes: list[str], keyword: str) -> Documents:
        documents = self._client.index(uid=index_name).search(keyword, {"attributesToHighlight": attributes})
        return documents["hits"]


class TaskStatus(str, Enum):
    Succeeded = "succeeded"
    Failed = "failed"


class URLAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "URL already exists"


class InvalidDocumentError(Exception):
    pass
