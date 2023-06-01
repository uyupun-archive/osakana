from fastapi import APIRouter, Depends
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from api.errors.docs import http_422_error_res_doc
from api.schemas.reading_list import ReadingListSearchResponse
from db.repos.reading_list import ReadingListRepository

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.get(
    "",
    response_model=ReadingListSearchResponse,
    responses={
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc(),
    },
)
def search(
    keyword: str,
    is_bookmarked: bool = False,
    is_read: bool = False,
    is_unread: bool = False,
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListSearchResponse:
    """
    リーディングリストの検索
    """
    reading_list = repo.search(
        keyword=keyword,
        is_bookmarked=is_bookmarked,
        is_read=is_read,
        is_unread=is_unread,
    )
    return reading_list
