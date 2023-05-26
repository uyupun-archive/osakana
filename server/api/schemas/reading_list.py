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


UnsignedInteger = conint(strict=True, ge=0)


class ReadingListCountsResponse(BaseModel):
    total: UnsignedInteger  # type: ignore
    reads: UnsignedInteger  # type: ignore
    unreads: UnsignedInteger  # type: ignore
    bookmarks: UnsignedInteger  # type: ignore


ReadingListExportResponse = list[ReadingListRecord]
