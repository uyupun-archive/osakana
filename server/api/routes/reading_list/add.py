from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from api.errors.docs import (
    http_404_error_res_doc,
    http_409_error_res_doc,
    http_422_error_res_doc,
)
from api.schemas.reading_list import ReadingListAddRequest, ReadingListAddResponse
from db.models.reading_list import ReadingListRecord
from db.repos.reading_list import ReadingListRepository
from services.web_scraping import (
    FaviconNotFoundError,
    IconNotFoundError,
    TitleNotFoundError,
    WebScrapingService,
)

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post(
    "",
    response_model=ReadingListAddResponse,
    responses={
        HTTP_404_NOT_FOUND: http_404_error_res_doc(
            desc="WebPageAccessError Response",
            message="404 Client Error: Not Found for url: https://example.com",
        ),
        HTTP_409_CONFLICT: http_409_error_res_doc(
            desc="UrlAlreadyExistsError Response", message="URL already exists"
        ),
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc(),
    },
)
def add(
    req: ReadingListAddRequest,
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
    service: WebScrapingService = Depends(WebScrapingService.create_service),
) -> ReadingListAddResponse:
    """
    リーディングリストに追加
    """
    service.fetch(url=req.url)

    try:
        title = service.get_title()
    except TitleNotFoundError:
        title = "No title"

    try:
        thumb = service.get_favicon_link()
    except (IconNotFoundError, FaviconNotFoundError):
        thumb = None

    new_reading_list_record = ReadingListRecord(url=req.url, title=title, thumb=thumb)
    repo.add(reading_list_record=new_reading_list_record)
    return ReadingListAddResponse()
