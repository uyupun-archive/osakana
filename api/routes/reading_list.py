from fastapi import APIRouter, Depends

from api.schemas.reading_list import (ReadingListAddRequest, ReadingListAddResponse, ReadingListSearchResponse)
from db.repos.reading_list import ReadingListRepository
from deps import get_reading_list_repository


router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post("", response_model=ReadingListAddResponse)
def add(req: ReadingListAddRequest, repo: ReadingListRepository=Depends(get_reading_list_repository)) -> ReadingListAddResponse:
    """
    リーディングリストに追加
    """
    print(repo)
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
