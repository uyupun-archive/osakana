from enum import Enum

from pydantic import BaseModel, HttpUrl


class ReadingListStatus(str, Enum):
    YET = "YET"
    DONE = "DONE"


class ReadingList(BaseModel):
    url: HttpUrl
    title: str
    status: ReadingListStatus
