from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, HttpUrl

from timezone import get_timezone


class ReadingListRecord(BaseModel):
    # id: str = ""
    url: HttpUrl
    title: str
    is_read: bool
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def set_timestamps(self, timezone: ZoneInfo=get_timezone()) -> None:
        self.created_at = datetime.now(tz=timezone)
        self.updated_at = datetime.now(tz=timezone)

class ReadingListIndex(BaseModel):
    url: HttpUrl
    title: str
