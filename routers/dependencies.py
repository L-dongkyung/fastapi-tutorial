from fastapi import APIRouter, Depends


router = APIRouter(
    prefix='/depends'
)


async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@router.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@router.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons