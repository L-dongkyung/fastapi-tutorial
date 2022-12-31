from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/debug"
)


@router.get("/{item_id}")
async def get_item(item_id: int):
    return JSONResponse(status_code=200, content=dict(item_id=item_id))
