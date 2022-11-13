from typing import Union

from fastapi import APIRouter, Body
from pydantic import BaseModel


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
