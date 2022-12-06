from datetime import datetime
from typing import Union

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


router = APIRouter(
    prefix='/encode_json'
)

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


@router.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    json_item = jsonable_encoder(item)
    fake_db[item_id] = json_item
    return {"item": [item_id, json_item]}
