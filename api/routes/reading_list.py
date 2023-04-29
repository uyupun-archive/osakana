from fastapi import APIRouter, Depends

from api.schemas.reading_list import (ReadingListAddRequest, ReadingListAddResponse, ReadingListSearchResponse)
from db.client import DBClient
from deps import get_db_client


router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post("", response_model=ReadingListAddResponse)
def add(req: ReadingListAddRequest, db_client: DBClient=Depends(get_db_client)) -> ReadingListAddResponse:
    """
    リーディングリストに追加
    """
    print(db_client)
    # TODO: URLからタイトルを取得する
    # TODO: URLからラベルを生成する
    # TODO: URL、タイトル、ラベル、ステータス、追加/更新日時をDBに保存する
    return ReadingListAddResponse(message=req.url)


@router.get("", response_model=ReadingListSearchResponse)
def search(label: str) -> ReadingListSearchResponse:
    """
    リーディングリストの検索
    """
    # TODO: ラベルで検索する
    return ReadingListSearchResponse(message=label)
