from dataclasses import dataclass
from typing import Union

from fastapi import APIRouter


@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None


router = APIRouter()


@router.post("/items/")
async def create_item(item: Item):
    return item
