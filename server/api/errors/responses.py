from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY


class APIError(BaseModel):
    status_code: int
    message: str

    def response(self):
        return JSONResponse(status_code=self.status_code, content=self.dict())


http_422_response_doc: dict[int | str, dict[str, Any]] = {HTTP_422_UNPROCESSABLE_ENTITY: {
    "description": "Validation error",
    "model": APIError,
    "content": {
        "application/json": {
            "example": {
                "status_code": HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "field required"
            }
        }
    }
}}
