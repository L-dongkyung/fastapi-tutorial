from fastapi import APIRouter, Depends, Cookie

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


class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/class_items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip:commons.skip + commons.limit]
    response.update({"items": items})
    return response


def query_extractor(q: str = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: str = Cookie(default=None)
):
    if not q:
        return last_query
    return q


@router.get("/sub/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}