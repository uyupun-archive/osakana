from fastapi import APIRouter, Depends

from api.schemas.reading_list import ReadingListExportResponse
from db.repos.reading_list import ReadingListRepository

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.get("/export", response_model=ReadingListExportResponse)
def export(
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListExportResponse:
    """
    全てのリーディングリストを取得する
    """
    reading_list = repo.all()
    return reading_list
