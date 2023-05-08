from fastapi import FastAPI, Request
from starlette.status import HTTP_400_BAD_REQUEST

from errors.responses import APIError
from db.client import URLAlreadyExistsError, DocumentNotFoundError
from db.repos.reading_list import ReadingListRecordAlreadyReadError, ReadingListRecordAlreadyUnreadError
from lib.scraper import WebPageAccessError


async def url_already_exists_error_handler(req: Request, e: URLAlreadyExistsError):
    return APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)


async def web_page_access_error_handler(req: Request, e: WebPageAccessError):
    return APIError(status_code=e.status_code, message=e.message)


async def reading_list_record_already_read_error_handler(req: Request, e: ReadingListRecordAlreadyReadError):
    return APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)


async def reading_list_record_already_unread_error_handler(req: Request, e: ReadingListRecordAlreadyUnreadError):
    return APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)


async def document_not_found_error_handler(req: Request, e: DocumentNotFoundError):
    return APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(URLAlreadyExistsError, url_already_exists_error_handler)
    app.add_exception_handler(WebPageAccessError, web_page_access_error_handler)
    app.add_exception_handler(ReadingListRecordAlreadyReadError, reading_list_record_already_read_error_handler)
    app.add_exception_handler(ReadingListRecordAlreadyUnreadError, reading_list_record_already_unread_error_handler)
    app.add_exception_handler(DocumentNotFoundError, document_not_found_error_handler)
