from pydantic import BaseModel, HttpUrl


class ReadingListRecord(BaseModel):
    url: HttpUrl
    title: str
    is_read: bool


class ReadingListIndex(BaseModel):
    url: HttpUrl
    title: str
