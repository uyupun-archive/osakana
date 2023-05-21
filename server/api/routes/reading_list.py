from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from api.errors.responses import (
    http_403_error_res_doc,
    http_404_error_res_doc,
    http_409_error_res_doc,
    http_422_error_res_doc
)
from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListSearchResponse,
    ReadingListFishingResponse,
    ReadingListReadResponse,
    ReadingListUnreadResponse,
    ReadingListDeleteResponse,
    ReadingListBookmarkResponse
)
from db.models.reading_list import ReadingListRecord
from db.repos.reading_list import ReadingListRepository
from lib.scraper import (
    WebPageScraper,
    TitleNotFoundError,
    IconNotFoundError,
    FaviconNotFoundError
)


router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post("", response_model=ReadingListAddResponse, responses={
    HTTP_404_NOT_FOUND: http_404_error_res_doc,
    HTTP_409_CONFLICT: http_409_error_res_doc,
    HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
})
def add(
    req: ReadingListAddRequest,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository),
    scraper: WebPageScraper=Depends(WebPageScraper.create_scraper)
) -> ReadingListAddResponse:
    """
    リーディングリストに追加
    """
    scraper.fetch(url=req.url)

    try:
        title = scraper.get_title()
    except TitleNotFoundError:
        title = "No title"

    try:
        thumb = scraper.get_favicon_link()
    except (IconNotFoundError, FaviconNotFoundError):
        thumb = None

    new_reading_list_record = ReadingListRecord(url=req.url, title=title, thumb=thumb)
    repo.add(reading_list_record=new_reading_list_record)
    return ReadingListAddResponse()


@router.get("", response_model=ReadingListSearchResponse, responses={
    HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
})
def search(
    keyword: str,
    is_bookmarked: bool=False,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListSearchResponse:
    """
    リーディングリストの検索
    """
    reading_list = repo.search(keyword=keyword, is_bookmarked=is_bookmarked)
    return reading_list


@router.get("/fishing", response_model=ReadingListFishingResponse, responses={
    HTTP_404_NOT_FOUND: http_404_error_res_doc,
})
def fishing(
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListFishingResponse:
    """
    リーディングリストからランダムに１件取得
    """
    reading_list_record = repo.random()
    return reading_list_record


@router.patch("/read/{id}", response_model=ReadingListReadResponse, responses={
    HTTP_403_FORBIDDEN: http_403_error_res_doc,
    HTTP_404_NOT_FOUND: http_404_error_res_doc,
    HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
})
def read(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListReadResponse:
    """
    既読にする
    """
    repo.read(id=id)
    return ReadingListReadResponse()


@router.patch("/unread/{id}", response_model=ReadingListUnreadResponse, responses={
    HTTP_403_FORBIDDEN: http_403_error_res_doc,
    HTTP_404_NOT_FOUND: http_404_error_res_doc,
    HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
})
def unread(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListUnreadResponse:
    """
    未読にする
    """
    repo.unread(id=id)
    return ReadingListUnreadResponse()


@router.delete("/{id}", response_model=ReadingListDeleteResponse, responses={
    HTTP_404_NOT_FOUND: http_404_error_res_doc,
    HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
})
def delete(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListDeleteResponse:
    """
    リーディングリストから削除
    """
    repo.delete(id=id)
    return ReadingListDeleteResponse()


@router.patch("/bookmark/{id}", response_model=ReadingListBookmarkResponse, responses={
    HTTP_404_NOT_FOUND: http_404_error_res_doc,
    HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
})
def bookmark(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListBookmarkResponse:
    """
    ブックマークする
    """
    repo.bookmark(id=id)
    return ReadingListBookmarkResponse()
