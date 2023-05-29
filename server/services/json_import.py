from __future__ import annotations

import json
import os
from typing import Any

from fastapi import UploadFile
from pydantic import ValidationError

from db.models.reading_list import PrivateReadingList, PrivateReadingListRecord


class JsonImportService:
    max_file_size = 1024 * 1024 * 10  # 10MB

    def __init__(self):
        self._file: UploadFile | None = None
        self._contents: bytes = b""
        self._json_contents: Any = None
        self._private_reading_list: PrivateReadingList | None = None

    async def import_(self, file: UploadFile) -> PrivateReadingList:
        self._file = file
        await self._validate()
        self._parse()
        assert self._private_reading_list is not None
        return self._private_reading_list

    async def _validate(self) -> None:
        if self._file is None:
            raise FileNotExistsError()
        if self._file.filename is None:
            raise FileNameNotExistsError()

        self._contents = await self._file.read()
        self._validate_empty_file()
        self._validate_file_size()
        self._validate_file_extension()
        self._validate_contents()
        self._json_contents = json.loads(self._contents)
        self._validate_structure()

    def _validate_empty_file(self) -> None:
        if not self._contents:
            raise FileEmptyError()

    def _validate_file_size(self) -> None:
        if len(self._contents) > self.max_file_size:
            raise FileSizeLimitExceededError()

    def _validate_file_extension(self) -> None:
        assert self._file is not None
        assert self._file.filename is not None

        _, file_extension = os.path.splitext(self._file.filename)
        if file_extension != ".json":
            raise InvalidJsonFileExtensionError()

    def _validate_contents(self) -> None:
        try:
            self._json_contents = json.loads(self._contents)
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise InvalidJsonContentsError()

    def _validate_structure(self) -> None:
        if not isinstance(self._json_contents, list):
            raise InvalidJsonStructureError()

        for content in self._json_contents:
            if not isinstance(content, dict):
                raise InvalidJsonStructureError()
            for key in content.keys():
                if not isinstance(key, str):
                    raise InvalidJsonStructureError()

    def _parse(self) -> None:
        try:
            private_reading_list = [
                PrivateReadingListRecord(**content) for content in self._json_contents
            ]
        except ValidationError:
            raise PrivateReadingListRecordParseError()

        self._private_reading_list = private_reading_list


class FileEmptyError(Exception):
    pass


class FileNotExistsError(Exception):
    pass


class FileNameNotExistsError(Exception):
    pass


class InvalidJsonFileExtensionError(Exception):
    pass


class FileSizeLimitExceededError(Exception):
    pass


class InvalidJsonContentsError(Exception):
    pass


class InvalidJsonStructureError(Exception):
    pass


class PrivateReadingListRecordParseError(Exception):
    pass
