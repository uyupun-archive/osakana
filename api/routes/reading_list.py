from fastapi import APIRouter, Depends, HTTPException

from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListSearchResponse
)
from db.models.reading_list import ReadingList, ReadingListStatus
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
        raise HTTPException(status_code=400, detail=str(e))
    except TitleNotFoundError:
        title = "No title"

    reading_list = ReadingList(
        url=req.url,
        title=title,
        status=ReadingListStatus.YET
    )
    repo.add(reading_list=reading_list)
    return ReadingListAddResponse(message=req.url)


@router.get("", response_model=ReadingListSearchResponse)
def search(label: str) -> ReadingListSearchResponse:
    """
    リーディングリストの検索
    """
    # TODO: ラベルで検索する
    return ReadingListSearchResponse(message=label)
