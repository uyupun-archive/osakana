from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
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
from services.web_scraping import WebPageAccessError


async def validation_error_handler(
    req: Request, e: RequestValidationError
) -> JSONResponse:
    messages = ", ".join(error["msg"] for error in e.errors())
    return ApiError(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY, message=messages
    ).response()


async def url_already_exists_error_handler(
    req: Request, e: UrlAlreadyExistsError
) -> JSONResponse:
    return ApiError(status_code=HTTP_409_CONFLICT, message=e.message).response()


async def web_page_access_error_handler(
    req: Request, e: WebPageAccessError
) -> JSONResponse:
    return ApiError(status_code=e.status_code, message=e.message).response()


async def reading_list_record_already_read_error_handler(
    req: Request, e: ReadingListRecordAlreadyReadError
) -> JSONResponse:
    return ApiError(status_code=HTTP_403_FORBIDDEN, message=e.message).response()


async def reading_list_record_not_yet_read_error_handler(
    req: Request, e: ReadingListRecordNotYetReadError
) -> JSONResponse:
    return ApiError(status_code=HTTP_403_FORBIDDEN, message=e.message).response()


async def reading_list_record_not_found_error_handler(
    req: Request, e: ReadingListRecordNotFoundError
) -> JSONResponse:
    return ApiError(status_code=HTTP_404_NOT_FOUND, message=e.message).response()


async def internal_server_error_handler(req: Request, e: Exception) -> JSONResponse:
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
        exc_class_or_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        handler=internal_server_error_handler,
    )
