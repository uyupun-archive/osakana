from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


class ApiError(BaseModel):
    status_code: int
    message: str

    @validator("status_code")
    def validate_status_code(cls, status_code: int):
        if status_code < 400 or status_code > 599:
            raise ValueError()
        return status_code

    def response(self):
        return JSONResponse(status_code=self.status_code, content=self.dict())


def _create_error_res_doc(desc: str, status_code: int, message: str) -> dict[str, Any]:
    return {
        "description": desc,
        "model": ApiError,
        "content": {
            "application/json": {
                "example": {"status_code": status_code, "message": message}
            }
        },
    }


def http_400_error_res_doc(desc: str = "", message: str = "") -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_400_BAD_REQUEST,
        message=message,
    )


def http_403_error_res_doc(desc: str = "", message: str = "") -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_403_FORBIDDEN,
        message=message,
    )


def http_404_error_res_doc(desc: str = "", message: str = "") -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_404_NOT_FOUND,
        message=message,
    )


def http_409_error_res_doc(desc: str = "", message: str = "") -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_409_CONFLICT,
        message=message,
    )


def http_413_error_res_doc(desc: str = "", message: str = "") -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        message=message,
    )


def http_415_error_res_doc(desc: str = "", message: str = "") -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        message=message,
    )


def http_422_error_res_doc(
    desc: str = "Validation error", message: str = "field required"
) -> dict[str, Any]:
    return _create_error_res_doc(
        desc=desc,
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        message=message,
    )
