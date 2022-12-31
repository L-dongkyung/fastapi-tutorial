import yaml

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, ValidationError


router = APIRouter(
    prefix="/oper_config"
)


@router.get("/", operation_id="oper_config_id_define")
async def read_item():
    return {"item_id": "FOO"}


@router.get("/item/", include_in_schema=False)
async def read_items():
    return [{"item_id": "FOO"}]


@router.delete("/item/{item_id}")
async def delete_item(item_id):
    """
    Delete item
    \f this section show?
    :param item_id:
    :return:
    """
    return "deleted item"


@router.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    data = magic_data_reader(raw_body)
    return data


def magic_data_reader(raw_body: bytes):
    return {
        "size": len(raw_body),
        "content": {
            "name": "Maaaagic",
            "price": 42,
            "description": "Just kiddin', no magic here. ✨",
        },
    }


class Item(BaseModel):
    name: str
    tags: list[str]


@router.put(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.schema()}},
            "required": True,
        },
    },
)
async def update_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.parse_obj(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return item
