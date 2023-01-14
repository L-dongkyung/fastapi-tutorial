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

## Return a Response Directly
경로의 응답값으로 `dict`, `list`, `pydantic model`, `database model` 등을 직접적으로 반환 할 수 있습니다.  
FastAPI는 [JSON Compatible Encoder](https://fastapi.tiangolo.com/ko/tutorial/encoder/)에서 설명한 `jsonable_encoder`를
통해서 변환한 데이터를 `JSONResponse`에 담아 응답을 전송할 수 있습니다.  
또한, 이 JSON호환 데이터를 이용하여 사용자지정 헤더, 쿠키를 반환하는데 `JSONResponse`로 직접 응답을 보내는 것이 유용할 수 있습니다.  
```python
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    ...

@app.put("/item/")
async def read_item(item: Item):
    json_item = jsonable_encoder(item)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_item)
```
> database model의 경우 `Config`설정을 통해서 직접 응답에 입력할 수 있습니다.  
> 하지만 pydantic model은 직접 응답에 전할 할 수 없고 `dict`로 변환하여 전달해야합니다.  
> 그리고 `JSONResponse`는 `Response`를 상속받은 객체입니다.

`Response`를 통해 직접 응답을 전달 할 수 있습니다.
이를 통해 응답을 전달 할 경우 어떠한 변환을 하지 않고, 사용자의 의도대로 반환하기 때문에 유연성을 보장합니다.  
모든 데이터유형을 반환하고 데이터 선언 또는 유효성 감사를 재정의 할 수 있습니다.
```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
```

## Custom Response - HTML, Stream, File, others
###### 해당 파트는 코드로 작성하지 않았습니다. 설명에 fastapi 공식문서의 예제를 똑같이 옮겨왔습니다.
사용자 지정 응답을 통해 다양한 응답을 반환할 수 있습니다.  
`ORJSONResponse`, `HTMLResponse`, `Response`, `Custom Response` 등이 있습니다.  

### `ORJSONResponse`
성능을 극대화 하기 위해서 `orjson`을 사용하여 응답을 보낼 수 있습니다.  
`orjson`은 파이썬 내장 `json`보다 성능적으로 우수한 것으로 알려져 있습니다.(특정 상황에 한정적일 수 있음.)  
dict응답을 보낼 경우에 fastapi는 데이터를 jsonable한지 확인하는 과정에서 오버헤드가 발생합니다.  
그래서 `jsonable_encoder`을 사용하여 json객체를 반환 하는 것이 성능적으로 우수합니다.  
```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])
```

### `HTMLResponse`
HTML을 응답으로 보내야 할 경우 `HTMLResponse`를 사용하면 됩니다.
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
```
또는 return에 `HTMLResponse`를 사용할 수도 있습니다.
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
```

### `Response`
`Respons`를 이용하여 다른 응답을 반환하거나 사용자 지정 응답을 사용할 수 있습니다.  
매개변수는 아래와 같습니다.
* `content`: `str` or `bytes`. 반환 데이터를 전달합니다.
* `status_code`: `int`. 응답코드 번호를 입력합니다.
* `headers`: `dict`. 헤더에 입력되는 데이터를 전달합니다.
* `media_type`: `str`. 응답데이터의 유형을 전달합니다. (e.g. 'application/json')  

FastAPI에서는 이 `Response`객체를 상속받아서 많은 응답 객체를 정의 하였습니다.
* `HTMLResponse`
* `PlainTextResponse`
* `JSONResponse`
* `ORJSONResponse`
* `UJSONResponse`
* `RedirectResponse`
* `StreamingResponse`
* `FileResponse`  
이 객체들 모드 `fastapi.responses`에 위치해 있어 import 하여 사용할 수 있습니다.  

### `Custom Response`
응답을 직접 정의하여 사용할 수 있습니다.  
`Response`객체를 상속받아 클래스를 정의 하고 `response_class`파라미터에 선언합니다.
```python
from typing import Any

import orjson
from fastapi import FastAPI, Response

app = FastAPI()


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}
```

지금까지 다양한 사용자정의 응답에 대해서 서술하였습니다.  
이 사용자 정의 응답을 기본값으로 정의 하기 위해서는 `default_response_class`를 정의합니다.  
```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)
```

## Additional Responses in OpenAPI
위에서 응답을 바로 보내는 경우를 기술하였습니다.  
하지만 Swagger(OpenAPI)에서는 반영을 별도로 추가해야합니다.  
`responses`파라미터에 pydantic의 `BaseModel`을 이용해서 추가 할수 있습니다.  
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})
```
BaseModel을 schema로 입력할 경우 OpenAPI는 아래와 같은 응답을 생성합니다.
```bash
"responses": {
    "404": {
        "description": "Additional Response",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Message"
                }
            }
        }
    },
```
그리고 `"$ref": "#/components/schemas/Message"`이 schema는 OpenAPI 내부의 다른 위치를 참조합니다.  
```bash
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            ...
```

저는 이전의 status_code를 공부하면서 직접 입력하는 경우를 작성하였습니다.  
```bash
# ./endpoint/status_code.py line:29
responses={
        "404": {
            "description": "Not found item_id Response",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"},
                            "text": {"type": "string"}
                        }
                    }
                }
            }
        }
    })
```
를 이용하여 직접 입력할 수 있습니다.  

기존에 200 응답이 있는 경우 응답 유형을 추가 할 수 있습니다.  
아래의 경우 기존의 `response_medel`을 응답으로 반환하는 경우와 `image/png`로 응답하는 경우 2가지입니다.
```python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: Union[bool, None] = None):
    ...
```
> 기존의 응답에서 내용을 수정할 경우 해당 리소스를 덮어 쓰면 됩니다.  
> 위의 200응답에 description의 경우가 기존의 응답을 덮어쓰는 코드 입니다.

그리고 여러 응답을 한번에 추가 할 수 있습니다.  
```python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
...
```
기존에 여러 응답을 별도로 정의 하여 사용하고 추가로 응답을 추가할 경우
```python
responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
```
responses에 단순하게 추가만 하면 적용이 됩니다.

## Response Cookies
쿠키는 브라우저에서 저장하고 그 데이터를 요청시마다 헤더에 포함하여 서버로 전송합니다.  
> 만료일(expiration) 혹은 지속시간(dration)을 설정하여 정해진 시간에만 서버로 전송할 수 있으며,  
> 특정 도메인 혹은 경로제한을 설정할 수 있습니다.  

쿠키를 설정하는 방법은 파라미터로 response를 받아서 추가하는 방법과,  
처리 중간에 response를 선언하여 추가는 방법이 있습니다.  
두가지 모두 `Response`의 `set_cookie`함수를 이용하여 쿠키 데이터를 전송합니다.  
```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

# 1)
@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}

# 2)
@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
```
1. 응답을 파라미터로 정의하여 쿠키를 설정하고 응답으로 여러 데이터 형식을 정의 할수 있습니다.(e.g. pydantic model)
2. 응답을 코드 실행 중에 선언하여 쿠키와 응답 내용을 함께 설정합니다.  

이 두가지 방법을 이용할 수 있고, 응답에 반환하는 데이터에 따라서 선택하여 쿠키를 설정해야 합니다.  

## Response Headers
응답 헤더에 파라미터를 선언할 수 있습니다.  
이미 middle ware에서 헤더에 `X-Process-Time`을 추가하였습니다.  
이와 같은 방법으로 헤더에 파라미터를 추가 할 수 있습니다.  
```python
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

app = FastAPI()


@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}

@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
```
쿠키에 파라미터를 선언하는 방법과 동일하여 설명은 생략하겠습니다.  

## Response - Change Status Code
응답에서 `status_code`만 변경하고 싶은 경우가 있을 수 있습니다.  
응답 데이터는 기존의 방식을 유지하며 status-code를 바꾸고 싶을 경우 `Response`파라미터를 사용합니다.  
```python
from fastapi import FastAPI, Response, status

app = FastAPI()

tasks = {"foo": "Listen to the Bar Fighters"}


@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]
```
`Response`파라미터를 받은 후에 직접 `status_code`를 변경하고 응답을 보내면 됩니다.  

## Advanced Dependencies

> 이 내용은 인위적으로 보일 수 있다고 합니다. 또한, 어떻게 사용할지 명확하지 않을수 있습니다.  
> 하지만 예는 간단하고 어떻게 작동하는지 확인 할 수 있습니다.  
> 보안 파트에서 해당 부분의 사용예(JWT)가 나옵니다.  
> 이번에 로직을 이해했다면 보안 유틸리티 도구가 어떻게 작동하는지 이미 알고 있다고 합니다.  

```python
from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```
위 코드를 OpenAPI로 확인하면 `__call__`메소드의 파라미터`q`를 쿼리파라미터로 보내야합니다.  
그리고 그 내용에 `"bar"`가 있는지 확인합니다.  
fastapi는 `__call__`메소드의 파라미터를 경로작업함수에 추가합니다.  

`__init__`으로 객체를 파라미터화 하고 객체를 생성할 수 있습니다.  
그리고 그 객체를 종속성에 주입하면서 경로가 작업을 시작할때에 종속성에 의해 객체를 호출합니다.  
호출을 진행하면서 필요한 파라미터를 전달하고 결과 값을 반환합니다.  
1. 서버가 로드 되면서 객체를 생성하고 checker에 할당합니다.(생성된 객체의 id값은 변화가 없습니다.)
2. 경로 작업에 요청이 오면 `Depends`를 실행합니다.
3. 경로 작업은 checker를 호출합니다.
4. `checker(q=<params>)`로 q는 쿼리 파라미터로 전달 받습니다.
5. `__call__` 함수로 이동하고 코드블럭을 실행합니다.  


