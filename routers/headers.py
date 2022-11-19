from fastapi import Header, APIRouter

router = APIRouter(
    prefix='/headers',
)

@router.get('/items')
async def read_item(user: str = Header(default=None):
    return {"user": user}

@router.get('/list_items')
async def read_item(user: list[str] = Header(default=None):
    return {"user": user}

