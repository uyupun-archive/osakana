from fastapi import APIRouter
from schemas.ping import PingResponse

router = APIRouter(prefix="/ping", tags=["other"])


@router.get("", response_model=PingResponse)
def ping():
    """
    APIへの疎通確認
    """
    return {"message": "pong"}
