from pydantic import BaseModel, HttpUrl

from db.models.reading_list import ReadingListRecord


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    pass


ReadingListSearchResponse = list[ReadingListRecord]
