from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

router = APIRouter(
    prefix="/cookies"
)


@router.post("/cookie-object")
async def create_cookie(response: Response):
    response.set_cookie(key="cookie_key", value="cookie-value")
    return {"massage": "msg"}


@router.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response


class Item(BaseModel):
    id: str
    desc: str


@router.post("/cookie-object-test", response_model=Item)
async def create_cookie(item: Item, response: Response):
    response.set_cookie(key="cookie_key", value="cookie-value")
    return item
