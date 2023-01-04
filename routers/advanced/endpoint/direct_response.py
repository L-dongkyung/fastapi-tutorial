from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

router = APIRouter(
    prefix="/direct_response"
)

class Item(BaseModel):
    id: int
    name: str
    desc: str

    class Config:
        orm_mode = True

@router.post("/items/")
async def create_item(item: Item):
    json_item = jsonable_encoder(item)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_item)

# # 500 error
# @router.post("/items/")
# async def create_item(item: Item):
#     ...
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@router.get("/item/")
async def read_item():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
