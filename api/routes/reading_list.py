from fastapi import APIRouter, Depends
from starlette.status import HTTP_400_BAD_REQUEST

from api.errors import APIError
from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListSearchResponse
)
from db.client import URLAlreadyExistsError
from db.models.reading_list import ReadingListRecord
from db.repos.reading_list import ReadingListRepository
from scraper import WebPageScraper, WebPageAccessError, TitleNotFoundError


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
    try:
        title = scraper.get_title()
    except WebPageAccessError as e:
        raise APIError(status_code=e.status_code, message=e.message)
    except TitleNotFoundError:
        title = "No title"

    new_reading_list_record = ReadingListRecord(url=req.url, title=title)

    try:
        created_reading_list_record = repo.add(reading_list_record=new_reading_list_record)
    except URLAlreadyExistsError as e:
        raise APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)

    return created_reading_list_record


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
