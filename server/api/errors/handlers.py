from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY

from api.errors.responses import APIError
from db.repos.reading_list import (
    UrlAlreadyExistsError,
    ReadingListRecordAlreadyReadError,
    ReadingListRecordNotYetReadError,
    ReadingListRecordNotFoundError
)
from lib.scraper import WebPageAccessError


async def validation_error_handler(req: Request, e: RequestValidationError):
    messages = ", ".join(error["msg"] for error in e.errors())
    return APIError(status_code=HTTP_422_UNPROCESSABLE_ENTITY, message=messages).response()


async def url_already_exists_error_handler(req: Request, e: UrlAlreadyExistsError):
    return APIError(status_code=HTTP_409_CONFLICT, message=e.message).response()


async def web_page_access_error_handler(req: Request, e: WebPageAccessError):
    return APIError(status_code=e.status_code, message=e.message).response()


async def reading_list_record_already_read_error_handler(req: Request, e: ReadingListRecordAlreadyReadError):
    return APIError(status_code=HTTP_403_FORBIDDEN, message=e.message).response()


async def reading_list_record_not_yet_read_error_handler(req: Request, e: ReadingListRecordNotYetReadError):
    return APIError(status_code=HTTP_403_FORBIDDEN, message=e.message).response()


async def reading_list_record_not_found_error_handler(req: Request, e: ReadingListRecordNotFoundError):
    return APIError(status_code=HTTP_404_NOT_FOUND, message=e.message).response()


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(UrlAlreadyExistsError, url_already_exists_error_handler)
    app.add_exception_handler(WebPageAccessError, web_page_access_error_handler)
    app.add_exception_handler(ReadingListRecordAlreadyReadError, reading_list_record_already_read_error_handler)
    app.add_exception_handler(ReadingListRecordNotYetReadError, reading_list_record_not_yet_read_error_handler)
    app.add_exception_handler(ReadingListRecordNotFoundError, reading_list_record_not_found_error_handler)
