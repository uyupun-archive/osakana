from fastapi import APIRouter, Depends, File, UploadFile
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from api.errors.docs import (
    http_400_error_res_doc,
    http_409_error_res_doc,
    http_413_error_res_doc,
    http_415_error_res_doc,
    http_422_error_res_doc,
)
from api.schemas.reading_list import ReadingListImportResponse
from db.repos.reading_list import ReadingListRepository
from services.json_import import JsonImportService

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post(
    "/import",
    response_model=ReadingListImportResponse,
    responses={
        HTTP_400_BAD_REQUEST: http_400_error_res_doc(
            desc=(
                "EmptyFileError | "
                "InvalidJsonContentsError | "
                "InvalidJsonStructureError Response"
            ),
            message="Empty file",
        ),
        HTTP_409_CONFLICT: http_409_error_res_doc(
            desc="ReadingListRecordDuplicateError Response",
            message="Reading list record duplicate",
        ),
        HTTP_413_REQUEST_ENTITY_TOO_LARGE: http_413_error_res_doc(
            desc="FileSizeLimitExceededError Response",
            message="File size limit exceeded",
        ),
        HTTP_415_UNSUPPORTED_MEDIA_TYPE: http_415_error_res_doc(
            desc="InvalidFileExtensionError Response", message="Invalid file extension"
        ),
        HTTP_422_UNPROCESSABLE_ENTITY: http_422_error_res_doc(
            desc="ValidationError | PrivateReadingListRecordParseError Response"
        ),
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
