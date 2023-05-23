from pydantic import BaseModel, HttpUrl, conint

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


class ReadingListCountsResponse(BaseModel):
    reads: conint(ge=0)
    unreads: conint(ge=0)
    bookmarks: conint(ge=0)
