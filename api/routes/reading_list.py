from fastapi import APIRouter, Depends
from starlette.status import HTTP_400_BAD_REQUEST

from api.errors import APIError
from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListSearchResponse,
    ReadingListFeelingResponse,
    ReadingListReadRequest,
    ReadingListReadResponse
)
from db.client import URLAlreadyExistsError
from db.models.reading_list import ReadingListRecord
from db.repos.reading_list import ReadingListRepository
from lib.scraper import (
    WebPageScraper,
    WebPageAccessError,
    TitleNotFoundError,
    IconNotFoundError,
    FaviconNotFoundError
)


router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post("", response_model=ReadingListAddResponse)
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

    try:
        repo.add(reading_list_record=new_reading_list_record)
    except URLAlreadyExistsError as e:
        raise APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)

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
def random(
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListFeelingResponse:
    """
    リーディングリストからランダムに１件取得
    """
    reading_list_record = repo.random()
    return reading_list_record


@router.patch("/read", response_model=ReadingListReadResponse)
def read(
    req: ReadingListReadRequest,
    repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)
) -> ReadingListReadResponse:
    """
    既読にする
    """
    reading_list_record = repo.find(id=req.id)
    repo.read(reading_list_record=reading_list_record)
    return ReadingListReadResponse()
