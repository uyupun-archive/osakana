from uuid import UUID

from fastapi import APIRouter, Depends

from api.errors.responses import http_422_response_doc
from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListSearchResponse,
    ReadingListFeelingResponse,
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


@router.post("", response_model=ReadingListAddRequest, responses=http_422_response_doc)
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


@router.get("", response_model=ReadingListSearchResponse)
def search(
    keyword: str,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListSearchResponse:
    """
    リーディングリストの検索
    """
    reading_list = repo.search(keyword=keyword)
    return reading_list


@router.get("/feeling", response_model=ReadingListFeelingResponse)
def feeling(
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListFeelingResponse:
    """
    リーディングリストからランダムに１件取得
    """
    reading_list_record = repo.random()
    return reading_list_record


@router.patch("/read/{id}", response_model=ReadingListReadResponse)
def read(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListReadResponse:
    """
    既読にする
    """
    repo.read(id=id)
    return ReadingListReadResponse()


@router.patch("/unread/{id}", response_model=ReadingListUnreadResponse)
def unread(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListUnreadResponse:
    """
    未読にする
    """
    repo.unread(id=id)
    return ReadingListUnreadResponse()


@router.delete("/{id}", response_model=ReadingListDeleteResponse)
def delete(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListDeleteResponse:
    """
    リーディングリストから削除
    """
    repo.delete(id=id)
    return ReadingListDeleteResponse()


@router.patch("/bookmark/{id}", response_model=ReadingListBookmarkResponse)
def bookmark(
    id: UUID,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListBookmarkResponse:
    """
    ブックマークする
    """
    repo.bookmark(id=id)
    return ReadingListBookmarkResponse()
