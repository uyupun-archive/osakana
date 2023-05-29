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


http_400_error_res_doc = _create_error_res_doc(
    desc="Empty file error",
    status_code=HTTP_400_BAD_REQUEST,
    message="Empty file",
)


http_403_error_res_doc = _create_error_res_doc(
    desc="Reading list record already read error",
    status_code=HTTP_403_FORBIDDEN,
    message="Reading list record already read",
)


http_404_error_res_doc = _create_error_res_doc(
    desc="Web page access error",
    status_code=HTTP_404_NOT_FOUND,
    message="404 Client Error: Not Found for url: https://example.com",
)


http_409_error_res_doc = _create_error_res_doc(
    desc="URL already exists error",
    status_code=HTTP_409_CONFLICT,
    message="URL already exists",
)


http_413_error_res_doc = _create_error_res_doc(
    desc="File size limit exceeded error",
    status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    message="File size limit exceeded",
)


http_415_error_res_doc = _create_error_res_doc(
    desc="Invalid file extension error",
    status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    message="Invalid file extension",
)


http_422_error_res_doc = _create_error_res_doc(
    desc="Validation error",
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    message="field required",
)
