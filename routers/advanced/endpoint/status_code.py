from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/status"
)


items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@router.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: str = Body(default=None),
    size: int = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


# @router.delete("/items/{item_id}",
#                responses={
#                    "404": {
#                        "description": "Not found item_id Response",
#                        "content": {
#                            "application/json": {
#                                "schema": {
#                                    "type": "object",
#                                    "properties": {
#                                        "message": {"type": "string"},
#                                        "text": {"type": "string"}
#                                    }
#                                }
#                            }
#                        }
#                    }
#                })
# async def delete_item(item_id):
#     if item_id in items:
#         return JSONResponse(status_code=200, content="Deleted item")
#     else:
#         return JSONResponse(status_code=404, content="Not found item")
