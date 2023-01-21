from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/request"
)


@router.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}


@router.get("/")
def read_request(request: Request):
    req_data = request.headers
    a = type(req_data)
    return {"a": req_data}
