from pydantic import BaseModel


class ListAddResponse(BaseModel):
    message: str


class ListSearchResponse(BaseModel):
    message: str
