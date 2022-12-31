from enum import Enum

from typing import Union

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix='/oper_conf'
)


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()


@router.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

class Tags(Enum):
    items = "items"
    users = "users"


@router.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@router.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]


@router.post(
    "/items_kwargs/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item


@router.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@router.post(
    "/items_add_response_desc/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    return item


@router.get("/elements/", deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
