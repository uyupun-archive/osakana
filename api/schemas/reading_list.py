from pydantic import BaseModel, HttpUrl


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    message: str


class ReadingListSearchResponse(BaseModel):
    message: str
