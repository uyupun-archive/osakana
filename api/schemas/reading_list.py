from uuid import UUID

from pydantic import BaseModel, HttpUrl

from db.models.reading_list import ReadingListRecord


class ReadingListAddRequest(BaseModel):
    url: HttpUrl


class ReadingListAddResponse(BaseModel):
    pass


ReadingListSearchResponse = list[ReadingListRecord]


ReadingListFeelingResponse = ReadingListRecord


class ReadingListReadRequest(BaseModel):
    id: UUID


class ReadingListReadResponse(BaseModel):
    pass


class ReadingListUnreadRequest(BaseModel):
    id: UUID


class ReadingListUnreadResponse(BaseModel):
    pass


class ReadingListDeleteResponse(BaseModel):
    pass


class ReadingListBookmarkResponse(BaseModel):
    pass
