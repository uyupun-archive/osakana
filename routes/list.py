from fastapi import APIRouter
from schemas.list import ListAddResponse, ListSearchResponse


router = APIRouter(prefix="/list", tags=["list"])


@router.post("", response_model=ListAddResponse)
def add():
    """
    リーディングリストに追加
    """
    return {"message": "pong"}


@router.get("", response_model=ListSearchResponse)
def search():
    """
    リーディングリストの検索
    """
    return {"message": "pong"}
