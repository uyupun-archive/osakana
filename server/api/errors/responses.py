from fastapi.responses import JSONResponse
from pydantic import BaseModel


class APIError(BaseModel):
    status_code: int
    message: str

    def response(self):
        return JSONResponse(status_code=self.status_code, content=self.dict())
