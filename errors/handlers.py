from fastapi import Request
from starlette.status import HTTP_400_BAD_REQUEST

from errors.responses import APIError
from db.client import URLAlreadyExistsError
from lib.scraper import WebPageAccessError


async def url_already_error_handler(req: Request, e: URLAlreadyExistsError):
    return APIError(status_code=HTTP_400_BAD_REQUEST, message=e.message)


async def web_page_access_error_handler(req: Request, e: WebPageAccessError):
    return APIError(status_code=e.status_code, message=e.message)
