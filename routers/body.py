from typing import Union

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field


router = APIRouter(
    prefix='/body'
)


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@router.post("/create_items/")
async def create_item(item: Item):
    return item


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# 나열 자료형(list, set)의 타입정의.
class Tags(BaseModel):
    tags: list[str] = []
    keyword: set[str] = set()

@router.post("/tags/")
async def get_tags(tags: Tags):
    return {"tags": tags, "tags": tags.tags}

@router.get("/keyword/")
async def get_keyword(tags: Tags):
    return {"tags": tags, "keyword": tags.keyword}


# 모델 내포를 통한 다른 모델 정의
class Image(BaseModel):
    url: str
    name: str


class ImageItem(BaseModel):
    name: str
    description: str = None
    image: Image = None


@router.post("/image_item/")
async def get_image_item(item: ImageItem):
    return {"image_item": item}


# 특별 타입의 검증
from pydantic import HttpUrl

class Docs(BaseModel):
    url: HttpUrl
    name: str


@router.post("/docs/")
async def get_docs(docs: Docs):
    return {"docs": docs}


# list안에 모델 자료형 정의.
@router.post("/images/multi")
async def multi_images(images: list[Image]):
    return {"images": images}


# dict의 자료형 정의.
@router.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


# Config 클래스 정의를 통한 예시 설정.
class SchemaExtra(BaseModel):
    name: str
    desc: str

    class Config:
        schema_extra = {
            "example": {
                "name": "foo",
                "desc": "bar",
            }
        }


@router.put("/schema/")
async def config_schema(schema: SchemaExtra):
    return {"schema": schema}


# Field를 통한 예시 설정.
class ExField(BaseModel):
    name: str = Field(example="foo")
    desc: str = Field(example="bar")


@router.put("/field/")
async def ex_field(ex: ExField):
    return {"ex_field": ex}


# Body를 이용한 예시 설정/
@router.post("/body_ex/")
async def body_ex(ex: Item = Body(
    example={
        "name": "foo",
        "desc": "bar"
    }
)):
    return {"ex_body": ex}


# 여러 예시들을 적용은 body에서만 적용 가능.
class MultiExampleBody(BaseModel):
    name: str = None
    desc: str = None


@router.post("/multi_ex_body/")
async def multi_ex(ex: MultiExampleBody = Body(
    examples={
        "normal": {
            "summary": "title1",
            "description": "description title",
            "value": {
                "name": "foo",
                "desc": "bar"
            }
        },
        "converted": {
            "summary": "title2",
            "description": "desc title2",
            "value": {
                "name": "converted",
                "desc": "conv"
            }
        }
    }
)):
    return {"multi_ex": ex}

#  Config 클래스로는 여러 예시 적용 불가.
# class MultiExampleSchema(BaseModel):
#     name: str = None
#     desc: str = None
#
#     class Config:
#         schema_extra = {
#             "examples": {
#                 "normal":{
#                     "summary": "schema_title",
#                     "description": "schema desc",
#                     "value": {
#                         "name": "normal name",
#                         "desc": "normal desc"
#                     }
#                 },
#                 "conv":{
#                     "summary": "schema_title2",
#                     "description": "schema_desc2",
#                     "value": {
#                         "name": "conv name",
#                         "desc": "conv desc",
#                     }
#                 }
#             }
#         }
#
#
# @router.put("/multi_ex_schema/")
# async def multi_ex_schema(ex: MultiExampleSchema):
#     return {"multi_ex": ex}



