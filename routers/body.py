from typing import Union

from fastapi import APIRouter
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
