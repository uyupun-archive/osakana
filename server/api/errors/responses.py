from pydantic import BaseModel


class APIError(BaseModel):
    status_code: int
    message: str
