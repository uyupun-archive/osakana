from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator


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
