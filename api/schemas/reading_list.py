from pydantic import BaseModel, HttpUrl


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    inserted_id: str
    url: HttpUrl
    title: str


class ReadingListSearchRow(BaseModel):
    id: str
    url: HttpUrl
    title: str
    is_read: bool
    created_at: str
    updated_at: str


class ReadingListSearchResponse(BaseModel):
    reading_list: list[ReadingListSearchRow]
