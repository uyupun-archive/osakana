from pydantic import BaseModel, HttpUrl

from db.models.reading_list import ReadingListRecord


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


ReadingListAddResponse = ReadingListRecord


ReadingListSearchResponse = list[ReadingListRecord]
