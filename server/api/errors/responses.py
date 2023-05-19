from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY


class APIError(BaseModel):
    status_code: int
    message: str

    def response(self):
        return JSONResponse(status_code=self.status_code, content=self.dict())


def _create_error_res_doc(desc: str, status_code: int, message: str) -> dict[str, Any]:
    return {
        "description": desc,
        "model": APIError,
        "content": {
            "application/json": {
                "example": {
                    "status_code": status_code,
                    "message": message
                }
            }
        }
    }


http_403_error_res_doc = _create_error_res_doc(
    desc="Web page access error",
    status_code=HTTP_403_FORBIDDEN,
    message="Reading list record already read"
)


http_404_error_res_doc = _create_error_res_doc(
    desc="Web page access error",
    status_code=HTTP_404_NOT_FOUND,
    message="404 Client Error: Not Found for url: https://example.com"
)


http_409_error_res_doc = _create_error_res_doc(
    desc="URL already exists",
    status_code=HTTP_409_CONFLICT,
    message="URL already exists error"
)


http_422_error_res_doc = _create_error_res_doc(
    desc="Validation error",
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    message="field required"
)
