from pydantic import BaseModel, HttpUrl


class ReadingList(BaseModel):
    url: HttpUrl
    title: str
    is_read: bool


class ReadingListIndex(BaseModel):
    url: HttpUrl
    title: str
