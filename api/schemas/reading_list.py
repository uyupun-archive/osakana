from pydantic import BaseModel, HttpUrl


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    inserted_id: str
    url: HttpUrl
    title: str


class ReadingListSearchResponse(BaseModel):
    message: str
