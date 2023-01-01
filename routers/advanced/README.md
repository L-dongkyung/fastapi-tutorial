[Before read tutorial](../../README.md)
# Advanced User Guide

---

## Path Operation Advanced Configuration
> OpenAPI 전문가 수준의 내용입니다. 저는 아직 이 내용에 대해서 이해하지 못했습니다.

### Operation id
OpenAPI(Swagger)의 operation id를 정의 할 수 있습니다.  
operation id를 확인하기 위해서는 `openapi_url`을 통해 JSON으로 확인 가능합니다.  
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_items():
    return [{"item_id": "Foo"}]
```

함수 이름으로 `operation id`를 지정할 수 있습니다.
```python
from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)
```

### Hide path operation
OpenAPI에서 경로를 제거할 수 있습니다.  
데코레이터에 `include_in_schema`를 `False`로 설정하면 OpenAPI에서 해당 경로는 사라집니다.  
하지만 요청은 가능하여 문서상 보안이 필요한 경로를 숨길 수 있습니다.
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/", include_in_schema=False)
async def item():
    return 
```

### Docstring config
독스트링에서 불필요한 부분을 삭제할 수 있습니다.  
`\f`를 통해서 이후에 나오는 내용을 OpenAPI에서 숨길수 있습니다.  
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    """
    read item response
    \f asdasdasdasd
    :param item_id: Item id
    """
```

### OpenAPI extra
pydantic을 선언하지 않고 schema를 입력할 수 있습니다.  
(pydantic validation을 사용할 수 없습니다.)
```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    return raw_body
```

### Custom OpenAPI content type
OpenAPI는 사용자가 요청 schema를 정의하여 사용할 수 있습니다.  
물론, 해당 요청의 데이터를 코드에서 실행 가능하게 변환해야합니다.
아래 예시는 `yaml`타입으로 요청을 받고 json으로 변환하여 pydantic모델을 생성합니다.  
```python
from typing import List

import yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError

app = FastAPI()


class Item(BaseModel):
    name: str
    tags: List[str]


@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.parse_obj(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return item
```
`yaml.safe_load()`를 통해서 body의 text를 dict로 변환합니다.  
`parse_obj`는 인수가 dict일 경우 모델을 생성합니다.  dict가 아닐경우 error 발생.  

## Additional Status Codes
응답에 대한 추가적인 `status code`를 반한화기 위해서는 `JSONResponse` 또는 `Response`를 사용하면 됩니다.  
```python
from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@app.get("/items/{item_id}")
async def read_item(item_id):
    if item_id in items:
        return items[item_id]
    else:
        JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"{item_id} not found")
```
`JSONResponse`를 통해서 다른 status code로 반환 할 수 있지만 OpenAPI에는 반영이 안되어 있습니다.  
OpenAPI에 추가하는 방법을 찾았지만 공식문서에서 차후에 다루기 때문에 잠시 후에 작성하겠습니다. (Additional Responses in OpenAPI)
