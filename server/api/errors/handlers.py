from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.errors.responses import ApiError
from db.repos.reading_list import (
    ReadingListRecordAlreadyReadError,
    ReadingListRecordNotFoundError,
    ReadingListRecordNotYetReadError,
    UrlAlreadyExistsError,
)
from services.json_import import (
    EmptyFileError,
    FileSizeLimitExceededError,
    InvalidFileExtensionError,
    InvalidJsonContentsError,
    InvalidJsonStructureError,
    PrivateReadingListRecordParseError,
)
from services.web_scraping import WebPageAccessError


def validation_error_handler(req: Request, e: RequestValidationError) -> JSONResponse:
    messages = ", ".join(error["msg"] for error in e.errors())
    return ApiError(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY, message=messages
    ).response()


def url_already_exists_error_handler(
    req: Request, e: UrlAlreadyExistsError
) -> JSONResponse:
    return ApiError(status_code=HTTP_409_CONFLICT, message=e.message).response()


def web_page_access_error_handler(req: Request, e: WebPageAccessError) -> JSONResponse:
    return ApiError(status_code=e.status_code, message=e.message).response()


def reading_list_record_already_read_error_handler(
    req: Request, e: ReadingListRecordAlreadyReadError
) -> JSONResponse:
    return ApiError(status_code=HTTP_403_FORBIDDEN, message=e.message).response()


def reading_list_record_not_yet_read_error_handler(
    req: Request, e: ReadingListRecordNotYetReadError
) -> JSONResponse:
    return ApiError(status_code=HTTP_403_FORBIDDEN, message=e.message).response()


def reading_list_record_not_found_error_handler(
    req: Request, e: ReadingListRecordNotFoundError
) -> JSONResponse:
    return ApiError(status_code=HTTP_404_NOT_FOUND, message=e.message).response()


def empty_file_error_handler(req: Request, e: EmptyFileError):
    return ApiError(status_code=HTTP_400_BAD_REQUEST, message=e.message).response()


def file_size_limit_exceeded_error_handler(req: Request, e: FileSizeLimitExceededError):
    return ApiError(
        status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE, message=e.message
    ).response()


def invalid_file_extension_error_handler(req: Request, e: InvalidFileExtensionError):
    return ApiError(
        status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE, message=e.message
    ).response()


def invalid_json_contents_error_handler(req: Request, e: InvalidJsonContentsError):
    return ApiError(status_code=HTTP_400_BAD_REQUEST, message=e.message).response()


def invalid_json_structure_error_handler(req: Request, e: InvalidJsonStructureError):
    return ApiError(status_code=HTTP_400_BAD_REQUEST, message=e.message).response()


def private_reading_list_record_parse_error_handler(
    req: Request, e: PrivateReadingListRecordParseError
):
    return ApiError(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY, message=e.message
    ).response()


def internal_server_error_handler(req: Request, e: Exception) -> JSONResponse:
    return ApiError(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR, message="Internal server error"
    ).response()


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=validation_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=UrlAlreadyExistsError,
        handler=url_already_exists_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=WebPageAccessError,
        handler=web_page_access_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=ReadingListRecordAlreadyReadError,
        handler=reading_list_record_already_read_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=ReadingListRecordNotYetReadError,
        handler=reading_list_record_not_yet_read_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=ReadingListRecordNotFoundError,
        handler=reading_list_record_not_found_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=EmptyFileError,
        handler=empty_file_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=FileSizeLimitExceededError,
        handler=file_size_limit_exceeded_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=InvalidFileExtensionError,
        handler=invalid_file_extension_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=InvalidJsonContentsError,
        handler=invalid_json_contents_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=InvalidJsonStructureError,
        handler=invalid_json_structure_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=PrivateReadingListRecordParseError,
        handler=private_reading_list_record_parse_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        handler=internal_server_error_handler,
    )
