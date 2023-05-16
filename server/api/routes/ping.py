from fastapi import APIRouter

from api.schemas.ping import PingResponse


router = APIRouter(prefix="/ping", tags=["other"])


@router.get("", response_model=PingResponse)
def ping() -> PingResponse:
    """
    APIへの疎通確認
    """
    return PingResponse(message="pong")
