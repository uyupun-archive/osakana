from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from api.errors.responses import (
    http_400_error_res_doc,
    http_403_error_res_doc,
    http_404_error_res_doc,
    http_409_error_res_doc,
    http_413_error_res_doc,
    http_415_error_res_doc,
    http_422_error_res_doc,
)
from api.schemas.reading_list import (
    ReadingListAddRequest,
    ReadingListAddResponse,
    ReadingListBookmarkResponse,
    ReadingListCountsResponse,
    ReadingListDeleteResponse,
    ReadingListExportResponse,
    ReadingListFishingResponse,
    ReadingListImportResponse,
    ReadingListReadResponse,
    ReadingListSearchResponse,
    ReadingListUnreadResponse,
)
from db.models.reading_list import ReadingListRecord
from db.repos.reading_list import ReadingListCountType, ReadingListRepository
from services.json_import import JsonImportService
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
        HTTP_404_NOT_FOUND: http_404_error_res_doc,
        HTTP_409_CONFLICT: http_409_error_res_doc,
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
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


@router.get(
    "",
    response_model=ReadingListSearchResponse,
    responses={
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
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


@router.get(
    "/fishing",
    response_model=ReadingListFishingResponse,
    responses={
        HTTP_404_NOT_FOUND: http_404_error_res_doc,
    },
)
def fishing(
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListFishingResponse:
    """
    リーディングリストからランダムに１件取得
    """
    reading_list_record = repo.random()
    return reading_list_record


@router.patch(
    "/read/{id}",
    response_model=ReadingListReadResponse,
    responses={
        HTTP_403_FORBIDDEN: http_403_error_res_doc,
        HTTP_404_NOT_FOUND: http_404_error_res_doc,
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
    },
)
def read(
    id: UUID,
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListReadResponse:
    """
    既読にする
    """
    repo.read(id=id)
    return ReadingListReadResponse()


@router.patch(
    "/unread/{id}",
    response_model=ReadingListUnreadResponse,
    responses={
        HTTP_403_FORBIDDEN: http_403_error_res_doc,
        HTTP_404_NOT_FOUND: http_404_error_res_doc,
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
    },
)
def unread(
    id: UUID,
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListUnreadResponse:
    """
    未読にする
    """
    repo.unread(id=id)
    return ReadingListUnreadResponse()


@router.delete(
    "/{id}",
    response_model=ReadingListDeleteResponse,
    responses={
        HTTP_404_NOT_FOUND: http_404_error_res_doc,
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
    },
)
def delete(
    id: UUID,
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListDeleteResponse:
    """
    リーディングリストから削除
    """
    repo.delete(id=id)
    return ReadingListDeleteResponse()


@router.patch(
    "/bookmark/{id}",
    response_model=ReadingListBookmarkResponse,
    responses={
        HTTP_404_NOT_FOUND: http_404_error_res_doc,
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
    },
)
def bookmark(
    id: UUID,
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListBookmarkResponse:
    """
    ブックマークする
    """
    repo.bookmark(id=id)
    return ReadingListBookmarkResponse()


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


@router.get("/export", response_model=ReadingListExportResponse)
def export(
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListExportResponse:
    """
    全てのリーディングリストを取得する
    """
    reading_list = repo.all()
    return reading_list


@router.post(
    "/import",
    response_model=ReadingListImportResponse,
    responses={
        HTTP_400_BAD_REQUEST: http_400_error_res_doc,
        HTTP_413_REQUEST_ENTITY_TOO_LARGE: http_413_error_res_doc,
        HTTP_415_UNSUPPORTED_MEDIA_TYPE: http_415_error_res_doc,
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc,
    },
)
async def import_(
    file: UploadFile = File(...),
    service: JsonImportService = Depends(JsonImportService),
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListImportResponse:
    private_reading_list = await service.import_(file=file)
    repo.bulk_add(private_reading_list=private_reading_list)

    return ReadingListImportResponse()
