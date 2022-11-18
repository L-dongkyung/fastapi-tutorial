from fastapi import APIRouter, Cookie

router = APIRouter(
    prefix="/cookie"
)


@router.get("/items/")
async def get_item(abs_id: str = Cookie()):
    return {"abs_id": abs_id}
