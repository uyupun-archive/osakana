from fastapi import HTTPException


class APIError(HTTPException):
    def __init__(self, status_code: int, message: Exception):
        detail = str(message)
        super().__init__(status_code=status_code, detail=detail)
