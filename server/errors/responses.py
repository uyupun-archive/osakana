from fastapi.responses import JSONResponse


class APIError(JSONResponse):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, content={"message": message})
