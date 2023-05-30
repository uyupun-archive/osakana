from __future__ import annotations

from abc import abstractclassmethod, abstractmethod

from pydantic import BaseModel

from db.client import Document


class OsakanaBaseModel(BaseModel):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def has_field(cls, field: str) -> str:
        fields = list(cls.__fields__.keys())
        if field in fields:
            return field
        raise FieldNotDefinedError()

    @abstractmethod
    def to_dict(cls, model: OsakanaBaseModel) -> Document:
        return Document()

    @abstractclassmethod
    def to_instance(cls, document: Document) -> OsakanaBaseModel:
        return OsakanaBaseModel()


class FieldNotDefinedError(Exception):
    pass
