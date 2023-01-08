from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

router = APIRouter(
    prefix="/open_api_response"
)


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


@router.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@router.get(
    "/item/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: bool = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}


@router.get(
    "/items/{item}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def read_item(item: str):
    if item == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
