from fastapi import APIRouter, Depends

from api.schemas.reading_list import ReadingListFishingResponse
from db.repos.reading_list import ReadingListRepository

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.get(
    "/fishing",
    response_model=ReadingListFishingResponse,
)
def fishing(
    repo: ReadingListRepository = Depends(ReadingListRepository.get_repository),
) -> ReadingListFishingResponse:
    """
    リーディングリストからランダムに１件取得
    """
    reading_list_record = repo.random()
    return reading_list_record
