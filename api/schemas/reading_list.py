from pydantic import BaseModel, HttpUrl

from db.models.reading_list import ReadingListRecord


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    reading_list_record: ReadingListRecord


class ReadingListSearchResponse(BaseModel):
    reading_list: list[ReadingListRecord]
