from fastapi import APIRouter, Request, HTTPException,
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/errors'
)

fake_item_db = {"foo": "foo item"}

@router.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_item_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "there goes my error?"}
        )
    return {"item": fake_item_db[item_id]}

