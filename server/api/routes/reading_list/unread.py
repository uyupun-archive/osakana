from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from api.errors.docs import (
    http_403_error_res_doc,
    http_404_error_res_doc,
    http_422_error_res_doc,
)
from api.schemas.reading_list import ReadingListUnreadResponse
from db.repos.reading_list import ReadingListRepository

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.patch(
    "/unread/{id}",
    response_model=ReadingListUnreadResponse,
    responses={
        HTTP_403_FORBIDDEN: http_403_error_res_doc(
            desc="ReadingListRecordAlreadyUnreadError Response",
            message="Reading list record already unread",
        ),
        HTTP_404_NOT_FOUND: http_404_error_res_doc(
            desc="ReadingListRecordNotFoundError Response",
            message="Reading list record not found",
        ),
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc(
            message="value is not a valid uuid"
        ),
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
