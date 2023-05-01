from fastapi import APIRouter, Depends
from starlette.status import HTTP_400_BAD_REQUEST

from api.errors import APIError
from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListSearchRow,
    ReadingListSearchResponse
)
from db.models.reading_list import ReadingList
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
        raise APIError(status_code=HTTP_400_BAD_REQUEST, message=e)
    except TitleNotFoundError:
        title = "No title"

    reading_list = ReadingList(
        url=req.url,
        title=title,
        is_read=False
    )
    inserted_id = repo.add(reading_list=reading_list)
    return ReadingListAddResponse(
        inserted_id=inserted_id,
        url=req.url,
        title=title
    )


@router.get("", response_model=ReadingListSearchResponse)
def search(keyword: str, repo: ReadingListRepository=Depends(ReadingListRepository.get_repository)) -> ReadingListSearchResponse:
    """
    リーディングリストの検索
    """
    reading_list = repo.search(keyword=keyword)
    rows = []
    for row in reading_list:
        rows.append(ReadingListSearchRow(
            id=str(row["_id"]),
            url=row["url"],
            title=row["title"],
            is_read=row["is_read"],
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"])
        ))
    print(rows)
    return ReadingListSearchResponse(reading_list=rows)
