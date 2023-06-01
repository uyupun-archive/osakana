from fastapi import APIRouter, Depends

from api.schemas.reading_list import ReadingListCountsResponse
from db.repos.reading_list import ReadingListCountType, ReadingListRepository

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.get("/counts", response_model=ReadingListCountsResponse)
def counts(
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListCountsResponse:
    """
    リーディングリスト全体の数、既読の数、未読の数、ブックマーク数を返す
    """
    total = repo.count(type=ReadingListCountType.IS_ALL)
    reads = repo.count(type=ReadingListCountType.IS_READ)
    unreads = repo.count(type=ReadingListCountType.IS_UNREAD)
    bookmarks = repo.count(type=ReadingListCountType.IS_BOOKMARKED)

    return ReadingListCountsResponse(
        total=total, reads=reads, unreads=unreads, bookmarks=bookmarks
    )
