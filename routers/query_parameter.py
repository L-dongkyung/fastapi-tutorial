from typing import Union

from fastapi import APIRouter


router = APIRouter(
    prefix='/query'
)

# 쿼리 매개변수 학습 DB
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@router.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


# 쿼리파라미터 선택적 입력.
@router.get("/items_q/{item_id}")
async def read_item_q(item_id: str, q: Union[str, None] = None):
    if q:
        return {'item_id': item_id, 'q': q}
    return {'item_id': item_id}


# bool자료형의 입력.
# bool형으로는 [1, 0, on, off, True, true, False, false, yes, no]을 받을 수 있습니다.
@router.get("/short/{short_id}")
async def short(short_id: str, short: bool = False):
    item = {'short_id': short_id}
    if not short:
        item.update({"desc": "This is an amazing item that has a long disc"})
    return item


# 필수 쿼리 매개변수
@router.get("/req_short/{short_id}")
async def short_req(short_id: str, needy: str):
    return {"short_id": short_id, "needy": needy}


# 선택으로 논값?
@router.get("/option_short/{short_id}")
async def opt_short(short_id: str, option: Union[int, None] = None):  # Union을 사용하는 것과 안쓰는 것의 차이는?
    return {'short_id': short_id, 'option': option}
