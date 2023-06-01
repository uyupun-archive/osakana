from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from api.errors.handlers import (
    empty_file_error_handler,
    file_size_limit_exceeded_error_handler,
    internal_server_error_handler,
    invalid_file_extension_error_handler,
    invalid_json_contents_error_handler,
    invalid_json_structure_error_handler,
    private_reading_list_record_parse_error_handler,
    reading_list_record_already_read_error_handler,
    reading_list_record_duplicate_error_handler,
    reading_list_record_not_found_error_handler,
    reading_list_record_not_yet_read_error_handler,
    url_already_exists_error_handler,
    validation_error_handler,
    web_page_access_error_handler,
)
from db.repos.reading_list import (
    ReadingListRecordAlreadyReadError,
    ReadingListRecordDuplicateError,
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
        exc_class_or_status_code=ReadingListRecordDuplicateError,
        handler=reading_list_record_duplicate_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        handler=internal_server_error_handler,
    )
