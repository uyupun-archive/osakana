from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from api.errors.docs import http_404_error_res_doc, http_422_error_res_doc
from api.schemas.reading_list import ReadingListDeleteResponse
from db.repos.reading_list import ReadingListRepository

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.delete(
    "/{id}",
    response_model=ReadingListDeleteResponse,
    responses={
        HTTP_404_NOT_FOUND: http_404_error_res_doc(
            desc="ReadingListRecordNotFoundError Response",
            message="Reading list record not found",
        ),
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc(
            message="value is not a valid uuid"
        ),
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
