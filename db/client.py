from time import sleep
from typing import Any

import meilisearch

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
        # TODO: URLのユニークチェック
        task_id = index.add_documents(documents=[document]).task_uid

        task_status = None
        while task_status != "succeeded":
            sleep(1)
            task_status = index.get_task(uid=task_id).status

            if task_status == "failed":
                raise InvalidDocumentError

    def search_documents(self, index_name: str, keyword: str) -> Documents:
        documents = self._client.index(uid=index_name).search(keyword, {"attributesToHighlight": ["title", "url"]})
        return documents["hits"]


class URLAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.message = "URL already exists"


class InvalidDocumentError(Exception):
    pass
