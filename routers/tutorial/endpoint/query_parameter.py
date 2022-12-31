from typing import Union

from fastapi import APIRouter, Query


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


# length Validation
@router.get("/validate_item")
async def validate_item(q: str = Query(max_length=50)):
    result = {'items': 'Foo'}
    if q:
        result.update({'q': q})
    return result


# Union클래스로는 Option요소 구성 불가능.
@router.get("/union_option")
async def use_union_option(q: Union[str, None] = Query(max_length=10)):
    print(type(q))
    return {"q": q}


# Ellipsis(...)를 이용하여 필수요소 정의.
@router.get("/ellipsis/")
async def use_ellipsis(q: str = Query(default=...)):
    return {'q': q}


# Query 클래스의 선택은?
@router.get("/option_item")
async def option_use_query(q: str = Query(default=None)):
    if q:
        return {"q": q}


# regex 사용
@router.get("/regex_ex")
async def regex(number:str = Query(regex="^[0-9]{3}-[0-9]{4}-[0-9]{4}$")):
    return {'phone_num': number}


# query 파라미터를 list로 받는 방법
@router.get("/reduplication_item/")
async def reduplication_item(q: list[str] = Query(default=None)):
    return {"q": q}
@router.get("/list_item/")
async def list_item(q: list[str] = Query(default=[])):
    return {"q": q}


# Title과 description
@router.get("/metadata_items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# alias를 이용해서 쿼리매개변수 매핑
@router.get("/alias_items")
async def read_items(q: Union[str, None] = Query(default=None, alias="item-query")):
    if q:
        return {"q": q}
    return None


# deprecated로 매개변수 사용 중단 표시
@router.get("/deprecated/")
async def deprecated_parameter(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        deprecated=True,
    )
):
    if q:
        return {'q': q}
    return None


# include_in_schema를 이용해서 매개변수 삭제
@router.get("/include_schema")
async def include_schema(
        q: str = Query(default=None, include_in_schema=False)
):
    if q:
        return {"q": q}
    return None