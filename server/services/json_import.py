from __future__ import annotations

import json
import os

from fastapi import UploadFile
from pydantic import ValidationError

from db.models.reading_list import PrivateReadingList, PrivateReadingListRecord


class JsonImportService:
    max_file_size = 1024 * 1024 * 10  # 10MB

    def __init__(self):
        self._file = None
        self._json_contents = None

    def create(self, file: UploadFile):
        self._file = file

    async def validate(self):
        if self._file is None:
            raise FileNotExistsError()

        if self._file.filename is None:
            raise FileNameNotExistsError()

        await self._validate_empty_file()
        self._validate_file_extension()
        await self._validate_contents()
        await self._validate_file_size()
        self._validate_structure()

    async def _validate_empty_file(self):
        assert self._file is not None

        contents = await self._file.read()
        if not contents:
            raise FileEmptyError()

    def _validate_file_extension(self):
        assert self._file is not None
        assert self._file.filename is not None

        _, file_extension = os.path.splitext(self._file.filename)
        if file_extension != ".json":
            raise InvalidJsonFileExtensionError()

    async def _validate_file_size(self):
        assert self._file is not None

        contents = await self._file.read()
        if len(contents) > self.max_file_size:
            raise FileSizeLimitExceededError()

    async def _validate_contents(self):
        assert self._file is not None

        contents = await self._file.read()
        try:
            self._json_contents = json.loads(contents)
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise InvalidJsonContentsError()

    def _validate_structure(self):
        if not isinstance(self._json_contents, list):
            raise InvalidJsonStructureError()

        for content in self._json_contents:
            if not isinstance(content, dict):
                raise InvalidJsonStructureError()
            for key in content.keys():
                if not isinstance(key, str):
                    raise InvalidJsonStructureError()

    def parse(self) -> PrivateReadingList:
        if self._json_contents is None:
            raise InvalidJsonContentsError()

        try:
            records = [
                PrivateReadingListRecord(**content) for content in self._json_contents
            ]
        except ValidationError:
            raise PrivateReadingListRecordParseError()

        return records


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
