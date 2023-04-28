from pydantic import BaseModel


class ListAddRequest(BaseModel):
    url: str


class ListAddResponse(BaseModel):
    message: str


class ListSearchResponse(BaseModel):
    message: str
