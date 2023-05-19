from pydantic import BaseModel, HttpUrl

from db.models.reading_list import ReadingListRecord


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    pass


ReadingListSearchResponse = list[ReadingListRecord]


ReadingListFishingResponse = ReadingListRecord


class ReadingListReadResponse(BaseModel):
    pass


class ReadingListUnreadResponse(BaseModel):
    pass


class ReadingListDeleteResponse(BaseModel):
    pass


class ReadingListBookmarkResponse(BaseModel):
    pass
