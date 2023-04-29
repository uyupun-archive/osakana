from fastapi import APIRouter, Depends

from schemas.list import ListAddRequest, ListAddResponse, ListSearchResponse
from deps import get_db_client


router = APIRouter(prefix="/list", tags=["list"])


@router.post("", response_model=ListAddResponse)
def add(req: ListAddRequest, db_client=Depends(get_db_client)):
    """
    リーディングリストに追加
    """
    print(db_client)
    # TODO: URLからタイトルを取得する
    # TODO: URLからラベルを生成する
    # TODO: URL、タイトル、ラベル、ステータス、追加/更新日時をDBに保存する
    return {"message": req.url}


@router.get("", response_model=ListSearchResponse)
def search(label: str):
    """
    リーディングリストの検索
    """
    # TODO: ラベルで検索する
    return {"message": label}
