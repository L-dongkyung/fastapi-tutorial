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

## OAuth2 scopes
OAuth2 범위를 fastapi에서 직접 사용할 수 있습니다.  
범위가 있는 OAuth2는 Facebook, Google, GitHub 등 많은 대규모 인증공급자가 사용합니다.  
> OAuth2 scopes가 반드시 필요하지 않습니다.  
> 대부분의 서비스는 OAuth2가 불필요하며 서비스의 복잡도를 올릴 수 있습니다.

OAuth2의 범위는 공백으로 구분된 문자열 목록입니다.  
각 범위의 이름은 모든 형식을 가질 수 있지만 윗줄의 이유로 공백을 사용하면 안됩니다.  
그리고 이 범위는 곧 권한을 나타냅니다.  

scopes 정의는 복잡하기 때문에 공식문서로 확인하는 것을 추천합니다.  
여기서는 간단히 그 로직에 대해서만 설명하겠습니다.
1. OAuth2PasswordBearer에 dict로 범위들을 정의 합니다. 이것은 OpenAPI에 추가됩니다.  
2. JWT 토큰에 scopes를 추가하여 token을 생성합니다.
3. 로그인 할 때에는 `Security`라는 `Depends`의 하위 클래스를 이용해서 유저와 scopes를 확인합니다.
4. `SecurityScopes`에 3번에서 전달 받은 scopes를 저장하고 token에 scope이 있는지 확인합니다.
5. 만약 scope이 없으면 필요한 scopes를 응답에 전달합니다.

> 공식문서에 조금더 자세하게 설명이 되어 있습니다. 하지만 큰 흐름을 이해하고 실서비스에 적용할 때에 다시 확인하는 것이 효율적으로 보입니다.  
> 그리고 자체 서비스가 아닌 외부 사용자가 있을 경우에는 더 복잡하고 흐름이 변경될 수 있습니다.

## HTTP Basic Auth
간단하게 HTTP 인증을 사용할 수 있습니다.  
HTTP 기본 인증 애플리케이션은 사용자이름(username), 비밀번호(password)가 포함된 헤더입니다.  
`WWW-Authenticate`의 헤더키에 `Basic`값이 들어가고 추가적으로 `realm`을 추가할 수 있습니다.  
```python
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
```
`HTTPBasicCredentials`를 이용해서 브라우저에 usesrname, password를 입력할 수 있게합니다.  

이를 통해서 유저를 검증하고 확인할 수 있습니다.  
```python
import secrets

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    ...
```
username, password 검증은 내장 함수인 `secrets`를 이용할 수 있습니다.(DB를 사용하면 필요 없어보입니다.)  
단순 str로 비교하여 검사 할 수 있지만 `Timing Attacks`에 내장 함수를 이용하는 것이 더 안전하다고 나와있습니다.  
> **Timing Attacks**  
> 단순 문자열 검증의 경우 문자열을 순차적으로 확인하고 다를 경우 False를 반환합니다.  
> 이 과정에서 첫번째 문자에서 반환하는 응답시간과 n번째 문자에서 반환하는 응답시간에 차이가 발생합니다.  
> 이를 이용하여 수천 또는 수백만번의 요청을 이용하여 알맞는 문자들을 찾아 재조합하여 username, password를 찾을 수 있습니다.

그리고 username, password가 다를 경우 에러를 반환하는데 이때에 401에러 반환해야합니다.  
예전에는 id, password 등 다른 부분을 찾아서 반환 하였지만 이는 보안에 취약해집니다.  
때문에 잘못된 정보가 입력되었을 경우에는 입력이 안된것과 같은 에러를 반환합니다.
```python
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Basic"},
)
```

## Using the Request Directly
앞의 미들웨어, 헤더 등에서 `Request`객체를 받아 데이터를 사용하거나 추가하였습니다.  
OpenAPI에서는 request 객체를 표현하지 않습니다. 하지만 다른 매개변수는 정상적으로 표현해줍니다.  
공식문서에서는 client의 host를 확인하는 코드가 작성되어 있습니다.  
```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
```
이미 헤더, 미들웨어, 쿠키 등을 통해 충분히 확인이 가능합니다.  
저는 Debug를 통해서 `Reauest` 객체에 다음과 같은 속성이 있는 것을 확인하였습니다.  
* app
* base_url
* client
* cookies
* headers
* method
* path_params
* query_params
* scope
* state
* url
* ...

OpenAPI를 통해 웹에서 간단히 확인한 것이고 모바일 또는 클라이언트(PC)에서 보낼 경우에 추가 또는 삭제 되는 속성이 있을 수 있습니다.  
그리고 저는 크로스 플랫폼을 구현할 경우에 `user-Agent`를 확인해야 한다고 알고 있습니다. 이것은 headers에 있습니다.(당연하지만 확인 했습니다.)  

## Using Dataclasses
fastapi에서 dataclass를 사용할 수 있습니다.  
```python
from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```
dataclass를 pydantic 모델에 사용할 수 있습니다.  
pydantic은 똑같이 사용할 수 있으며  
* 데이터 검증
* 데이터 직렬화(serialization)
* 데이터 문서화

또한 pydantic 모델처럼 `response_model`에 정의 할 수 있습니다.  
```python
from dataclasses import dataclass, field
from typing import List, Union

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be be playin' and havin' fun",
        "tags": ["breater"],
    }
```

또한 `dataclass`를 중첩구조로 사용할 수 있습니다.  
```python
from dataclasses import field  # 
from typing import List, Union

from fastapi import FastAPI
from pydantic.dataclasses import dataclass  # 


@dataclass
class Item:
    name: str
    description: Union[str, None] = None


@dataclass
class Author:
    name: str
    items: List[Item] = field(default_factory=list)  # 


app = FastAPI()


@app.post("/authors/{author_id}/items/", response_model=Author)  # 
async def create_author_items(author_id: str, items: List[Item]):  # 
    return {"name": author_id, "items": items}  # 


@app.get("/authors/", response_model=List[Author])  # 
def get_authors():  # 
    return [  # 
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]
```
사용은 직관적으로 보이기 때문에 위의 내용과 같이 사용하면 됩니다.

## Advanced Middleware
앞서 CORS와 사용자지정 미들웨어(process-time)을 추가하는 법을 배웠습니다.  
미들웨어는 app을 받아서 새로 앱을정의 할수도 있고,  
```python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```
fastapi에 middleware만 추가할 수 있습니다.(추천)  
```python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```
그리고 fastapi에서 지원해주는 middleware를 추가하여 사용할 수 있습니다.
* HTTPSRedirectMiddleware
* TrustedHostMiddleware
* GZipMiddleware
* ...

각 미들웨어의 사용법은 필요할 경우 확인하여 사용하는것이 좋을것으로 보입니다.  
정의된 미들웨어가 많고 사용방법에 차이가 있어서 미리 공부하는 것보다 필요할 경우 찾아서 추가하면 됩니다.  
기타 미들웨어로 `sentry`, `uvicorn's ProxyHeadersMiddleware`, `MassagePack` 등이 있습니다.  

## SQL (Relational) Databases with Peewee
> 초심자라면 `SQLAlchemy`로 충분합니다. Peewee는 생략하여도 됩니다.  
> Peewee를 안전하게 사용하려면 python3.7이상이 필요합니다.  

fastapi, peewee는 `threading.local`에 의존하고 있고, 직접 재정의하거나 연결/세션을 직접 처리할 수 있는 방법이 없습니다.  
하지만 Python3.7에서는 `contextvars`를 이용해서 새로운 비동기기능과 호환되는 `threading.local`을 적용할 수 있습니다.  

이것은 복잡해 보일 수 있지만 사용하기 위해 작동 방식을 완전히 이해할 필요는 없습니다.  

install
```
$ pip install peewee
```

peewee는 비동기 프레임워크용을 설계되지 않았습니다.  
그러나 비동기 프레임워크(e.g. FastAPI) 등에서 일부 기본값, 미리 정의된 데이터베이스의 지원 등을 수정해야할 때에  
복잡하고 많은 코드를 재정의 해야 합니다.  
그럼에도 불구하고 FastAPI와 Peewee를 이용해서 추가해야하는 코드를 확인 할 수 있습니다.  
```
파일 구조
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    └── schemas.py
```
파일 구조는 `SQLAlchemy`와 동일한 구조입니다.

database.py에 아래의 코드를 이용해서 DB를 정의 합니다.
```python
from contextvars import ContextVar

import peewee

DATABASE_NAME = "test.db"
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)

db._state = PeeweeConnectionState()
```
> `db = peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)`의 check_same_thread는 `SQLite`만 필요합니다.(SQLAlchemy도 동일)

PeeweeConnectionState()를 `db._state`에 덮어써서 사용합니다.

### Database model
그리고 SQLAlchemy에서 생성한것과 같은 model을 models.py에 정의합니다.
```python
import peewee

from .database import db


class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)

    class Meta:
        database = db


class Item(peewee.Model):
    title = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="items")

    class Meta:
        database = db
```
> peewee는 기본키(primary key)가 될 `id`에 정수 속성을 자동으로 추가합니다.
> `Item`클래스의 경우 선언하지 않아도 `User`클래스의 ID로 `owner_id`속성을 생성합니다.
> (외래키(Foreignkey)에 의해서 `owner_id`가 생성되는 것으로 예상합니다.)

### Pydantic model
SQLAlchemy와 같이 스키마 모델을 schemas.py에 생성합니다.
```python
from typing import Any, List, Union

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
```
SQLAlchemy와 동일하고 `PeeweeGetterDict`가 추가되었습니다.  
`user.items`를 사용하면 `peewee.ModelSelect`가 반환 됩니다. 이 타입은 generator로 `list`타입이 아니고, pydantic이 list로 변환하지 못합니다.  
하지만 `GetterDict`를 사용하여 `peewee.ModelSelect` 객체이면 `list`로 변환하여 반환 할 수 있습니다.  
이렇게 하기 위해서는 `Config`클래스에 `orm_mode = True`와 함께 `getter_dict = PeeweeGetterDict` 설정변수를 추가해야 합니다.  

### CRUD
CRUD도 SQLAlchemy와 동일합니다.  
```python
from . import models, schemas


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db_user.save()
    return db_user


def get_items(skip: int = 0, limit: int = 100):
    return list(models.Item.select().offset(skip).limit(limit))


def create_user_item(item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db_item.save()
    return db_item
```
하지만 SQLAlchemy처럼 db 클래스를 가져오지 않고 models을 직접 사용합니다.  
db 객체가 전역 객체로 정의되어 있어 모든 연결로직을 포함하고 있습니다. 그래서 `contextvars` 업데이트를 해야 합니다.  
또한, 여러 객체를 반환 할때에 `list`로 강제 형변환을 할 수 있습니다.  
```python
def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))
```
이렇게 할수 있는 이유는 `PeeweeGetterDict`를 정의하였기 때문입니다.  
그러나 경로작업에 `List[models.User]`로 `response_model`을 list로 정의하면 `Peewee.ModelSelect`로 반환하는 것이 아닌 response_model에 정의한 것으로 반환합니다.  
이것은 나중에 어떻게 작동하는지 보여질 것입니다.  

### Main
database 정의가 끝나면 main.py에서 모든 부분을 통합하여 서비스를 제공합니다.
```python
import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from . import crud, database, models, schemas
from .database import db_state_default

database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(skip=skip, limit=limit)
    return items


@app.get(
    "/slowusers/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    users = crud.get_users(skip=skip, limit=limit)
    return users
```
종속성을 통해 요청에 따른 DB connection을 생성해줍니다.  
```python
async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.post("/users/", dependencies=[Depends(get_db)])
def create_user(user):
    ...
```

SQLAlchemy와 비슷하게 `yield`를 통해서 connection을 연결하고 끝나면 `finally`를 통해서 close 해줍니다.  
SQLAlchemy와 다른 점은 db를 따로 사용하지 않습니다.  
SQLalchemy는 DB변수에서 모델 쿼리 등을 수행하지만 Peewee는 연결하고 그 응답을 사용하지 않기 때문에 데코레이터에 정의 하고 모델을 불러와 사용합니다.  

> peewee는 `async def`가 아닌 일반`def`를 사용하였습니다.  
> 때문에 db쿼리에 대해서 `await`을 안합니다.  
> async def와 일반 def의 차이는 나중에 자세히 다룰 것입니다.

### Testing Peewee with async
마지막으로 `database.py`의 `# db._state = PeeweeConnectionState()`과 `main.py`의  
```
async def reset_db_state():
#     database.db._state._state.set(db_state_default.copy())
#     database.db._state.reset()
    pass
```
부분을 주석처리하고 여러 요청을 보내면 중간에 서버에러를 발생합니다.  
해당 부분이 작동을 안하면서 동일한 스레드에서 작업을 진행하고 DB와 연결한다는 것을 확인 할 수 있습니다.  

> 공식문서에서는 이후 파일구조 및 코드를 점검합니다.  
> 그리고 `threading.local`과 `contextvars`에 대해서 설명합니다.  
> 마지막으로 `get_db()`를 통한 종속성 설정에 대해 기술되어있습니다.  
> [Technical Details](https://fastapi.tiangolo.com/ko/advanced/sql-databases-peewee/#technical-details)를 통해서 확인하면 좋을 것으로 보입니다.  

## NoSQL (Distributed / Big Data) Databases

FastAPI는 어떠한 NoSQL도 사용할 수 있습니다.  
하지만 공식 문서에서는 `Couchbase`라는 DB를 사용합니다.
* MongoDB
* Cassandra
* CouchDB
* ArangoDB
* ElasticSearch
> MongoDB를 이용한 FastAPI는 간단하게 구현하여 repo에 저장하였습니다.  
> [change_yaml_config](https://github.com/L-dongkyung/change_yaml_config)에서 MongoDB를 이용해서 yaml을 저장하고 수정하는 API를 정의하였습니다.  

### Couchbase install
```bash
pip install couchbase
```

### Use Couchbase

예시 코드는 아래와 같이 bucket을 연결하고 사용하면 됩니다.  
> import 에러가 발생하고 있습니다.  
> 버전에 따른 에러로 예상되고 실행테스트를 생략하겠습니다.  
> 전체적인 구현 흐름만 이해하고 저는 MongoDB를 이용해서 이미 NoSQL을 연결하였기 때문에 이 코드는 생략하겠습니다.
```python
from typing import Union

from couchbase import LOCKMODE_WAIT
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster, PasswordAuthenticator
from fastapi import FastAPI
from pydantic import BaseModel

USERPROFILE_DOC_TYPE = "userprofile"


def get_bucket():
    cluster = Cluster(
        "couchbase://couchbasehost:8091?fetch_mutation_tokens=1&operation_timeout=30&n1ql_timeout=300"
    )
    authenticator = PasswordAuthenticator("username", "password")
    cluster.authenticate(authenticator)
    bucket: Bucket = cluster.open_bucket("bucket_name", lockmode=LOCKMODE_WAIT)
    bucket.timeout = 30
    bucket.n1ql_timeout = 300
    return bucket


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str


def get_user(bucket: Bucket, username: str):
    doc_id = f"userprofile::{username}"
    result = bucket.get(doc_id, quiet=True)
    if not result.value:
        return None
    user = UserInDB(**result.value)
    return user


# FastAPI specific code
app = FastAPI()


@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    bucket = get_bucket()
    user = get_user(bucket=bucket, username=username)
    return user
```
couchbase의 bucket에 연결하는 `get_bucket`함수를 정의합니다.  
이 bucket으로 데이터를 처리할 것입니다.  

pydantic 모델을 정의 하고 하나의 `field`는 type으로 생성합니다.  
이것이 나중에 많은 도움이 될 것이라고 설명합니다.  

그리고 `get_user`로 user 정보를 조회하는 함수를 정의합니다.  
그 이후는 FastAPI의 endpoint를 정의하는 것과 같습니다.  

각 NoSQL마다 Python에 맞는 패키지가 있고 이를 이용해서 간편하게 FastAPI와 함께 사용할 수 있습니다.  
이번 절에서는 간단하게 코드를 보고 설명하여 NoSQL을 사용할 수 있는 것만 확인하였습니다.  

## Sub Applications - Mounts
Applicatio 마운트는 독립적은 OpenAPI를 가지는 두개의 앱을 연결하여 main 앱의 하위에 앱을 붙일 수 있습니다.  

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
```
코드에서 처럼 두개의 app을 정의 하고 main 앱에 `mount`함수를 이용하여 다른 앱을 붙일 수 있습니다.  
이를 이용해서 API문서를 나눌 수 있습니다. 경로는 mount할 경우에 입력하는 prefix가 추가되지만 요청에서는 크게 바뀌지 않습니다.  
> 문서를 나누는 부분에서는 많은 도움을 줄수 있을것 같습니다.  
> Fastapi는 tag의 하위 tag를 아직 지원하지 않습니다.  
> 그래서 하나의 tag에 endpoint가 많으면 관리가 쉽지 않지만 app단위로 먼저 문서를 나누고 tag로 다시 나누는 정도는 가능해 보입니다.  

또한, 하위 app에 다시 하위 app을 mount 할 수 있습니다.  

## Behind a Proxy
경우에 따라서 앱에 표시되지 않는 추가 접두사가 붙는 구성을 해야합니다.  
**Traefik**이나 **Nginx**와 같은 프록시 서버를 사용해야할 수 있습니다.  

fastapi의 `root_path`를 이 경우에 사용할 수 있습니다.  
두가지 방법으로 root_path를 정의 할 수 있습니다.  
### uvicorn에서 설정
```bash
$ uvicorn main:app --root-path /api/v1
```
위의 명령을 통해서 서버 오픈시에 root-path를 정의 할 수 있습니다.
### app 에서 설정
```python
from fastapi import FastAPI, Request

app = FastAPI(root_path="/api/v1")


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```
FastAPI 앱에서 root_path를 설정할 수 있습니다.

로컬에서 `Traefik`을 이용해서 테스트 할 수 있습니다.
traefik.toml파일을 아래와 같이 정의 합니다.
```toml
[entryPoints]
  [entryPoints.http]
    address = ":9999"

[providers]
  [providers.file]
    filename = "routes.toml"
```
routes.toml을 정의 합니다.
```toml
[http]
  [http.middlewares]

    [http.middlewares.api-stripprefix.stripPrefix]
      prefixes = ["/api/v1"]

  [http.routers]

    [http.routers.app-http]
      entryPoints = ["http"]
      service = "app"
      rule = "PathPrefix(`/api/v1`)"
      middlewares = ["api-stripprefix"]

  [http.services]

    [http.services.app]
      [http.services.app.loadBalancer]
        [[http.services.app.loadBalancer.servers]]
          url = "http://127.0.0.1:8000"
```
Traefik을 다운로드 받고 이를 실행합니다.
Assets에 많은 os별 파일이 있고 맞는 파일을 받아 압축을 풀면 하나의 파일이 있습니다. 이를 실행합니다.
```bash
./traefik --configFile=traefik.toml
```
traefik이 실행 중이면 fastapi app을 실행합니다.
```bash
uvicorn 메인:앱 --root-path /api/v1
```
이제 `http://127.0.0.1:8000/app/` 을 url에 검색하면 결과 값을 받을 수 있습니다.  
하지만 docs는 접근이 안될 것입니다.  

OpenAPI docs는 `http://127.0.0.1:9999/api/v1/docs` 를 입력하면 확인 할 수 있습니다.  
> 추가 서버가 있지만 이것은 나중에 다시 확인하겠습니다.  

## Templates
FastAPI도 모든 템플릿 엔진을 사용할 수 있습니다.  
일반적으로 사용하는 `jinja2`를 통해 템플릿을 구성하겠습니다.  
```bash
pip install jinja2
```
jinja2를 설치하고 임포트 하여 사용합니다.

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("../../static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
```
`fastapi.templating`에서 `Jinja2Templates`를 임포트하여 `templates`객체를 생성합니다.  
이 객체는 나중에 계속 사용할 수 있습니다.  
그리고 경로 파라미터에 응답 클래스를 정의 해서 docs UI에게 응답값으로 html을 전달한다고 알려줍니다.

template파일을 작성합니다.
```html
<html>
<head>
    <title>Item Details</title>
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
</head>
<body>
    <h1>Item ID: {{ id }}</h1>
</body>
</html>
```
그리고 스타일을 위한 css 파일을 작성합니다.
```css
h1 {
    color: green;
}
```
그리고 해당 경로를 url에 입력하면 html로 작성된 브라우저 창을 볼 수 있습니다.  
> ~~저는 `url_for`함수에서 경로(path)를 찾지 못하였습니다.~~  
> ~~나중에 경로를 찾는 방법을 확인하여 수정하겠습니다.~~  
> ~~url_for 문장(link태그)를 삭제하고 진행하면 html화면이 보입니다.~~  
> mount를 통해서 `static`폴더를 app에 추가하는데 이는 최상위 app에 있어야 인식하는 것으로 보입니다.  
> 만약 제가 틀렸거나 APIRouter에서 추가할 수 있는 방법을 아시는 분은 [email](mailto:ckldk91m@gmail.com)으로 연락주시기 바랍니다.  
> email: ckldk91m@gmail.com

## GraphQL
FastAPI는 ASGI를 표준으로 하고 있어서 ASGI와 호환되는 GraphQL라이브러리와 매우 쉽게 통합할 수 있습니다.  
> GraphQL은 일반적인 Web API와 비교할때 장점과 단점이 있습니다.  
> 이를 확인하여 장점이 단점보다 많은지 확인해야합니다.

GraphQL 라이브러리
* Strawberry
* Ariadne
* Tartiflette
* Graphene

GraphQL 중에서 Strawberry가 FastAPI의 디자인과 가장 유사하기 때문에 사용하기를 추천합니다.  
그리고 Strawberry 또한 Type annotation 기반입니다.  

### Strawberry install
```bash
pip install "strawberry-graphql[debug-server]"
```
간단한 예
```python
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)


schema = strawberry.Schema(query=Query)


graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
```
이를 통해서 graphql의 작동을 확인 할 수 있습니다.  
저는 역시 APIRouter를 이용해서 main:app에 연결하였지만,  
`http://127.0.0.1:8000/graphql` 를 통해서 작동을 확인 할 수 있었습니다.  
(`http://127.0.0.1:8000/advanced/graphql` 이 아닙니다.)  
> 이전 버전의 Starlette에 `GraphQLApp`이 있지만, Graphene으로 통합되었습니다.  
> Starlette에서는 이제 지원하지 않지만 이미 사용하고 있는 코드가 있다면 `starlette-graphene3`으로 이전하기 쉬울 것입니다.  

## WebSockets
간단하게 websocket을 설명하면 TCP 접속으로 통한 전 이중 통신 프로토콜입니다.  
http 통신을 이용해서 연결을 하고 그 이후 websocket으로 변환하여 클라이언트와 서버가 실시간 통신을 합니다.  

### Install
```bash
pip install websockets
```
React, Vue, Angular와 같은 프론트엔드를 구성하고 백엔드와 websocket 통신을 하는 것이 좋습니다.  
아래의 예에서는 js를 포함한 간단한 HTML를 통해 작동 방식에 대해서만 이해하고  
실제 production에서는 위의 옵션을 사용해야합니다.

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```
위의 코드에서는 html을 응답 받고 내부의 `script`를 통해서 `/ws`와 통신합니다.  
이를 통해서 간단하게 websocket의 작동을 확인할 수 있습니다.  

```python
from typing import Union

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    item_id: str,
    q: Union[int, None] = None,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
```
이 코드는 `Depends`를 통해서 인증이 이루어진 상황에만 통신을 연결합니다.
> WebSocketException은 fastapi가 아닌 websockets 라이브러리에서 import 해야하는 것으로 보입니다.

여러 클라이언트와 통신을 하는 코드는 아래와 같습니다.
```python
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
```
커넥션 리스트를 만들고 연결이 있을 경우 리스트에 추가합니다.  
그리고 manager 객체에서 이벤트가 발생할 경우 ws에 메세지를 전송합니다.

websocket에 대한 기본적인 작동 방식과 구조에 대해서 알아보았습니다.  

## Events: startup - shutdown
Application이 시작할 때 및 종료될 때에 실행해야하는 이벤트 핸들러를 정의 할 수 있습니다.

### startup
```python
from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
```
startup 이벤트는 app이 시작되기 전에 실행해야하는 함수로 `config`, `Database` 등을 사전에 정의 할 수 있습니다.  
startup 함수가 모두 완료 되기 전까지 app은 요청(request)를 수신하지 않습니다.

### shutdown
```python
from fastapi import FastAPI

app = FastAPI()


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")
```
app이 종료될 때에 수행해야하는 함수로 `DB Disconnect` 등 종료될때에 온전하게 종료할 수 있게 정의 합니다.  

## Custom Request and APIRoute class
사용자 지정 `Request`와 `APIRoute`를 정의 하여 사용할 수 있습니다.
이것의 사용사례는 아래와 같습니다.
* json이 아닌 요청본문을 json으로 변환합니다.
* gzip으로 압축된 본문의 압축을 풉니다.
* 모든 요청을 자동으로 기록합니다.

### GzipRequest 사용
gzip의 작동 방식을 보여줍니다. `GzipMiddleware`의 지원을 받을 수 있습니다.
```python
import gzip
from typing import Callable, List

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: List[int] = Body()):
    return {"sum": sum(numbers)}
```
먼저 `GzipRequest` 클래스를 정의합니다.  
request.body()를 덮어써서(overwrite) 헤더에 `Content-Encoding`에 gzip이 있는지 확인합니다.  
gzip이 있을 경우 압축을 풀고 없으면 그대로 return 합니다.  

그리고 `GzipRoute`를 정의합니다.  
상속받은 APIRoute의 `get_route_handler`를 overwrite 하고 내부에서 위에 선언한 `GzipRequest`를 이용하는 함수를 정의합니다.  
반환값으로 해당 함수를 실행하면서 함수 내부의 결과 값에 상속 받은 get_router_handler에 request를 전달합니다.  

### Accessing the request body in an exception handler
router에서의 예외처리도 같은 방식으로 진행 할 수 있습니다.
```python
from typing import Callable, List

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute


@app.post("/")
async def sum_numbers(numbers: List[int] = Body()):
    return sum(numbers)
```
예외가 발생하면 Request 인스턴스는 try 구문 안에 있기 때문에 except 구문을 실행 합니다.  
그리고 raise를 통해서 응답을 보냅니다.  
추가로 except의 body는 request 인스턴스를 다시 받아서 decode해서 응답을 보냅니다.  

### Custom APIRoute class in a router
또한, 사용자가 route에 기능을 추가할 수 있습니다.  
공식 문서에서는 request 의 시간을 측정하는 route를 구현하였습니다.  
```python
import time
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


app = FastAPI()
router = APIRouter(route_class=TimedRoute)


@app.get("/")
async def not_timed():
    return {"message": "Not timed"}


@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}


app.include_router(router)
```
> `super().get_route_handler()`함수를 기준으로 이전에는 요청의 전처리를, 이후에는 후처리를 진행합니다.  
> 또한 `route_class`를 정의하는 위치에 따라서 적용 유무가 발생합니다.  

## Testing WebSockets
websocket의 테스트는 app 과 동일하게 `TestClient`를 이용해서 진행할 수 있습니다.  
websocket의 연결을 유지하기 위해서 `with`문을 이용할 수 있습니다.  
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
```
공식 문서에 나와있는 코드를 통해 기본 작동 원리르 파악 할 수 있고,  
테스트는 기존에 작성한 `websocket.py`를 통해서 진행하겠습니다.  
```python
from fastapi.testclient import TestClient

from main import app


def test_websocket():
    test_client = TestClient(app)
    with test_client.websocket_connect("/advanced/ws/123") as ws:
        ws.send_text("asdf")
        data = ws.receive_text()
        assert data == "You wrote: asdf"
```
테스트 코드를 작성하고 main.py가 있는 곳에서 `pytest`를 진행하면 테스트 작업이 작동합니다.  
pytest 또는 unittest에 대한 설명은 나중에 하겠습니다.  
> 또한 작업을 진행하면서 postman에서 ws를 연결하는 방법을 찾았습니다.  
> 화면 왼쪽 제일 위에 my workspace가 있고 그 옆에 New를 누르면 websocket request가 있습니다.  
> 주소에 `ws://localhost:8000/advanced/ws/1111`을 입력하면 연결되고 Message에 글을 쓰면 작동합니다.  
> ![ws_postman_image](./ws_postman.png)

## Testing Events: startup - shutdown
startup 및 shutdown 이벤트에 대한 테스트를 진행 할 수 있습니다.
공식문서에서는 전역변수인 `items`에 데이터를 입력하고 그 데이터를 요청으로 받아서 확인합니다.
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}
```
tutorial에서 DB 초기화를 구현하지 않았는데 이부분을 구현하여 테스트해보면 좋을 것 같습니다.





