from enum import Enum

from pydantic import BaseModel, AnyHttpUrl


class ReadingListStatus(str, Enum):
    YET = "YET"
    DONE = "DONE"


class ReadingList(BaseModel):
    url: AnyHttpUrl
    title: str
    status: ReadingListStatus
