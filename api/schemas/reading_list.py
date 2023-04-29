from pydantic import BaseModel


class ReadingListAddRequest(BaseModel):
    url: str


class ReadingListAddResponse(BaseModel):
    message: str


class ReadingListSearchResponse(BaseModel):
    message: str
