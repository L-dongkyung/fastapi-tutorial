<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

# fastapi-tutorial

## fastapi install
```bash
$ pip install "fastapi[all]"
```
## path parameters
app 데코레이터의 경로에 parameter를 추가할 수 있습니다.  
url의 query string으로 전달 받은 str을 타입 선언을 할 경우 fastapi가 파싱합니다.  
타입 파싱에 실패할 경우 오류를 발생합니다.  
path의 parameter와 함수의 parameter명을 일치시켜야합니다.  
경로를 정의 할때에는 순서를 유의해야합니다.  
## Enum class
Enum 클래스를 사용하여 사전에 선택 값을 정의할 수 있습니다.
```python
from enum import Enum

class ClassName(Enum):
    ...
```
함수의 parameter 타입 어노테이션을 정의하여 경로 매개변수를 만듭니다.
## file path parameters
경로 파라미터에 `:path`를 추가하여 경로임을 선언합니다.  
이 경로 파라미터는 `/`로 시작하는 str이어야합니다.  
url의 경우 `server.com/files//home/dir/file.ext`형식으로 입력합니다.
```python
@app.get("/files/{file_path:path")
async def read_file(file_path: str):
    ...
```

## query parameters
경로(path) 파라미터와 함께 사용할 수 있습니다.  
`serer.com/path/path?key=value&key1=value1`의 형식으로 사용합니다.  
파라미터가 여러개일 경우 **&** 로 구분하여 추가합니다.  

Union 함수를 이용하거나 기본값을 설정하여 필수인지 선택인지 지정합니다.  

## Request Body
데이터를 body에 담아서 요청할 수 있습니다.  
Http Method는 POST, PUT, DELETE, PATCH을 사용합니다.  
`pydantic`의 `BaseModel`클래스를 이용하여 데이터 모델을 정의합니다.  
클래스의 필드에 type annotation을 지정합니다.
```python
from pydantic import BaseModel

class ModelName(BaseModel):
    field1: str
    field2: int
```
요청의 파라미터에 위의 데이터 클래스를 type annotation합니다.  
<br>

```python
@app.post('/path/')
async def funtion(param: ModelName):
    ...
```
parameter의 타입을 지정하는 것으로 FastAPI는 다음의 작업을 수행합니다.
* 인수의 데이터 값을 JSON으로 읽습니다.
* 정의된 type으로 변환합니다.
* 데이터를 검증합니다.
* 파라미터에 데이터를 전달합니다.

## API Router
main파일에 모든 API 엔드포인트를 정의하면 관리가 힘들어 파일별로 나눌 수 있습니다.  
이를 위해 APIRouter 클래스를 사용하고 prefix, tags 등 여러 옵션값을 정의할수 있습니다.  
```python
feater.py
from fastapi import APIRouter

router = APIRouter(prefix='/prefix', tags=['name'])

@router.get("/path")
async def funtion():
    ...
```
기능별로 구분한 파일에서 APIRouter클래스를 데코레이트하여 함수를 정의합니다.  
FastAPI클래스를 정의한 파일에서 기능정의한 클래스를 import하여  
include_router함수를 사용하여 app에 추가합니다.
```python
main.py
import feater

app.include_router(feater.router)
```

## Query Class validation
### 기본 사용법
쿼리 데이터의 검증을 fastapi의 `Query`클래스를 이용해서 할수 있습니다.  
```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: str = Query(min_length=3)):
    if q:
        return {"q": q}
```
### default
필수/옵션 파리미터의 경우 default 옵션으로 지정 가능합니다.  
일반적으로 필수요소의 경우 `default`를 사용하지 않으므로 `...`과 `Required`를 사용할 필요가 없습니다.
```python
from fastapi import FastAPI, Query
from pydantic import Required

@app.get("/items/")
async def read_items(q: str = Query(default=...|Required|None, min_length=3)):
    if q:
        return {"q": q}
```
* *...* 필수요소. Ellipsis로 필수요소를 표현합니다.
* *Required* 필수요소. pydantic에서 필수요소를 표현합니다.
* *None* 선택요소. 선택요소 표현으로 데이터가 없을 경우 None.
  * Query클래스를 정의할 경우 Union을 통한 선택요소 구성은 불가능합니다.
    ```python
    # Union으로 선택구성하였지만 필수요소로 정의됨.
    @app.get("/union_option")
    async def use_union_option(q: Union[str, None] = Query(max_length=10)):
        return {"q": q}
    ```
### 정규표현식
정규식을 통해서 입력 파라미터를 검증할 수 있습니다.  
정규식에 대해서는 사용하면서 공부하는 것도 하나의 방법입니다.
```python
@app.get("/regex_ex")
async def regex(number:str = Query(regex="^[0-9]{3}-[0-9]{4}-[0-9]{4}$")):
    return {'phone_num': number}
```
### list
쿼리스트링으로 리스트를 받는 방법은 두가지가 있습니다.  
1. 한 변수를 여러번 지정하여 값을 넘겨주는 방법.
2. 타입을 list로 지정하여 값들을 전달 받는 방법.
코드상에서는 다르게 표현하지만 url에서는 큰 차이가 없어보입니다.  
list 타입을 쿼리 매개변수로 받으려면 꼭 `Query`클래스를 명시적으로 사용해야합니다. 그렇지 않으면 `body` 매개변수로 해석합니다.
```python
@app.get("/reduplication_item/")
async def reduplication_item(q: list[str] = Query(default=None)):
    return {"q": q}
@app.get("/list_item/")
async def list_item(q: list[str] = Query(default=[])):
    return {"q": q}
```
### title, description
쿼리 매개변수에 title과 description을 추가할 수 있습니다.
이것은 매개변수에 대한 추가적인 데이터를 지정하는 것으로 예상됩니다.
```python
q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
```
### alias
alias를 이용한 파라미터 매핑을 할 수 있습니다.  
파이썬에서 사용할 수 없는 변수를 받아야할 경우 유용합니다.  
변수가 숫자로 시작하거나, -가 들어가있는 등.
```python
q: Union[str, None] = Query(default=None, alias="item-query")
```
### deprecated
deprecated를 이용해서 매개변수의 사용 중단을 문서(**docs**)에 표시할 수 있습니다.  
문서에서만 표시를 하고, 코드를 유지하면 계속 매개변수를 받습니다.
```python
q: Union[str, None] = Query(
    default=None,
    alias="item-query",
    deprecated=True,
)
```
### include_in_schema
include_in_schema를 이용해서 문서에서 해당 매개변수를 제외할 수 있습니다.  
서버에서 매개변수를 받아 처리할 수는 있어 서버의 변화는 없습니다.
```python
q: str = Query(default=None, include_in_schema=False)
```

## Path Class validation
Path 클래스의 사용법은 Query 클래스의 사용법과 유사합니다.  
### default
경로 매개변수는 경로의 일부이므로 무조건 필수요소입니다.  
default를 정의할 수 있지만 의미는 없습니다.  
```python
from fastapi import FastAPI, Path

@app.get("/items/{item_id}")
async def read_items(item_id: int = Path(default=None)):
    return {"item_id": item_id}
```
### 매개변수 정렬하기
파이썬에서 함수의 매개변수는 기본값이 없는 것을 앞에, 기본값이 있는 것을 뒤에 위치해야합니다.  
엔드포인트의 매개변수에 기본값이 없는 경우 필수요소로 정의합니다.  
Path 파라미터는 필요소요이므로 기본값을 정의 할 수도 있습니다.  
query 파라미터의 경우도 필수요소인 경우 기본값을 정의하지 않을 수 있습니다.  
이경우 query파라미터와 path 파라미터의 위치에 따라 파이썬에러가 발생할 수 있습니다.  
```python
@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    return {"item_id": item_id, "q": q}
```
위의 경우 Path 파라미터는 기본값을 가지고 있으므로 뒤에 위치 시킵니다.  
fastapi는 파라미터의 위치와 관계없이 알맞은 파라미터를 찾습니다.  
  
에스터리스크(*)을 사용하여 위치를 유지할수도 있습니다.  
에스터리스크는 뒤 따르는 매개변수들이 `kwargs`임을 정의하여 `key-value`의 형태를 가지게 합니다.  
따라서 기본값이 없는 경우에도 파이썬 에러가 발생하지 않습니다.
```python
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID"), q: str):
    return {"item_id": item_id, "q": q}
```

### 숫자 범위 검증
숫자를 매개변수로 받을때 이상, 초과, 이하, 미만을 정의할 수 있습니다.
* ge: 이상
* gt: 초과
* le: 이하
* lt: 미만
```python
@app.get("/items/{item_id}")
async def get_item(*, item_id: int = Path(ge=0, le=1000)):
    return {"item_id": item_id}
```

## Body Class validation
`Query` 및 `Path` 동등하게 `Body`클래스를 이용할 수 있습니다.  

### Singular values in body
Body 클래스는 단일요소를 매개변수로 받고 싶을때에 query 파라미터와의 구분을 위해 사용합니다.
```python
from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
  ...

@app.put("/items/")
async def update_item(item: Item, importance: int = Body()):
    return {"item": item, 'importance': importance}
```

### Embed a single body parameter
Embed 옵션을 통해서 내부에 정의되어 있음을 정의할 수 있습니다.
```python
class Item(BaseModel):
    ...

@app.put("/items/")
async def update_item(item: Item = Body(embed=True)):
    return {"item": item}
```

### Multiple body parameters
여러 데이터 모델을 정의하고 body에 여러 파라미터를 받을 수 있습니다.
```python
from pydantic import BaseModel
from fastapi import Body

class Item(BaseModel):
    ...

class User(BaseModel):
    ...

@app.put("/items/")
async def update_item(item: Item, user: User):
    ...
```

## list, set, dict의 자료형 정의.
```python
class item(BaseModel):
    name: str
    tags: list[str] = []
    keyword: set[str] = set()
    comment: dict[str, str] = {}
```
## 모델을 이용한 내장모델
자료형을 기본자료형 이외에 사용자 정의 자료형으로 설정할 수 있습니다.
```python
from pydantic import BaseModel

class Image(BaseModel):
    name: str
    url: str

class Item(BaseModel):
    name: str
    desc: str
    images: Image = None
```
## 특별한 자료형 검증
str, int, float 등 기본 자료형 이외에 pydantic에서 제공하는 많은 자료형이 있습니다.  
이를 이용해서 입력 데이터의 검증을 사전에 확인하고 코드의 복잡성을 줄일 수 있습니다.
[pydantic-docs](https://pydantic-docs.helpmanual.io/usage/types/)
* `HttpUrl`
* `Color`
* `EmailStr`
* `FilePath`
* `UUID`: 데이터베이스와 시스템에서 사용되는 공통 ID
* `datetime.datetime`: ISO 8601형식. `2008-09-15T15:53:00+05:00`
* `datetime.date`: `2008-09-15`
* `datetime.time`: `16:58:23.124`
* `frozenset`: request에서는 set으로 변환하고, response에서는 list로 변환
* `bytes`: 파이썬 표준 bytes타입의 str
* `Decimal`: 파이썬 표준 Decimal타입의 float

## 모델의 예시 정의
config, field, body의 세가지를 사용하여 예시를 적용할 수 있습니다.
### Config
```python
class Model(BaseModel):
    field1: str
    field2: str
    
    class Config:
        schema_extra = {
            "example": {
                "field1": "str",
                "field2": "str"
            }
        }
```
### field
```python
from pydantic import Field

class Model(BaseModel):
    field1: str = Field(example="str")
    field2: str = Field(example="str")
```
### body
```python
@app.put("/path/")
async def func(
        param: Class = Body(
            example={
                "field1": "str",
                "field2": "str"
            }
        )
):
    return 
```
### body를 통해 여러 예시 적용
```python
@app.put("/path/")
async def func(
        param: Class = Body(
            examples={
                "category": {
                    "summary": "title",
                    "description": "docs's desc",
                    "value": {
                        "field1": "str",
                        "field2": "str"
                    }
                },
                "category2": {
                    "summary": "title2",
                    "description": "docs's desc2",
                    "value": {
                        "field1": "str2",
                        "field2": "str2"
                    }
                }
            }
        )
):
    return 
```
## Cookie
쿠키를 파라미터로 받으려면 쿠키 클래스를 사용하여야합니다.  
쿠키 클래스를 사용하지 않으면 fastapi는 쿼리 파라미터로 인식합니다.
```python
from fastapi import Cookie

@app.get('/path')
async def get_path(cookie: str = Cookie(default=None)):
    return cookie
```
## Headers
헤터를 클래스를 이용해서 파라미터를 사용할 수 있습니다.  
```python
from fastapi import Header

@app.get('/headers')
async def funtion(q: str = Header()):
    return 
```
하나의 키에 여러개의 값이 있을 경우 list로 헤더 파라미터를 정의합니다.
```python
@app.get('/headers')
async def funtion(q: list[str] = Header()):
    return 
```
## Response Model
http요청의 `GET, POST, PUT, DELETE, etc`에 대한 응답 모델을 정의할 수 있습니다.  
`list[str]`과 같은 pydantic에서 지원하는 모델일 수 있지만 사용자 정의 모델을 사용할 수 있습니다.  
```python
class Class(BaseModel):
    field1: str
    field2: int

    
@app.get('/path', response_model=Class)
async def read_item(params):
    return params
```
### Response model의 데이터 선택
**Class로 구분**  
입력 model과 출력 model을 구분하여 정의할 수 있습니다.
```python
class InClass(BaseModel):
    field1: str
    field2: int


class OutClass(BaseModel):
    field1: str


@app.post('/create_items/', response_model=OutClass)
async def create_item(item: InClass):
    return item  # OutClass
```
*response model에서 기본값 선언이 안되어있는데 데이터의 키 값이 없으면 에러 발생.  

#### Parameter로 출력 데이터 선택
1. response_model_exclude_unset=\<bool>  
데이터의 키값이 response_model에 있는 항목만 반환합니다.
2. response_model_exclude_defaults=\<bool>  
데이터의 키값이 response_model에 기본값을 제외한 항목을 반환합니다.
3. response_model_exclude_none=\<bool\>  
데이터의 키값이 None인 항목을 제외하고 반환합니다.
4. response_model_include=\<set>  
response_model에서 반환할 field만 선택합니다.
5. response_model_exclude=\<set>  
response_model에서 반환하지 않을 field만 선택합니다.

*4, 5번은 set 대신에 list, tuple을 사용할 수 있지만 pycharm에서 주황색 context action경고가 표시됩니다.  

## Form
form 태그`<form></form>`를 사용하여 데이터를 받아올 경우에는 Form 클래스를 사용해야합니다.  
```python
from fastapi import Form

@app.post("/form/")
async def form(form_data: str = Form()):
    return form_data
```
form 클래스는 body클래스를 상속받았습니다.  
`Content-Type`은 `application/x-www-form-urlencoded`을 사용해야합니다.  

## File, UploadFile
`File`은 Form에서 상속받은 클래스입니다.  
매개변수가 쿼리나 body로 받는것을 방지하기위해 File()로 사용합니다.  
```python
from fastapi import File

@app.post("/file/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}
```
`UploadFile`은 동영상, 이미지 등 대용량 파일을 메모리를 소모하지 않고 처리하기에 적합합니다.  
UploadFile의 Attribute는
* `filename`: str로 파일명.
* `content_type`: str로 MIME type/media type.
* `file`: `SpooledTemporaryFile`객체입니다.
```python
from fastapi import UploadFile

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    return {"filename": file.filename}
```
UploadFile의 메소드를 이용해 파일을 제어할 수 있습니다.
* `write(data)`: data(str이나 bytes)를 파일에 작성합니다.
* `read(size)`: 파일 사이즈 또는 글자의 사이즈를 읽습니다.
* `seek(offset)`: 파일 내부의 offset위치의 파이트로 이동합니다.
* `close()`: 파일을 닫습니다.

위 메소드 들은 모두 `async` 메소드로 `await`과 함께 사용하여야합니다.  
```python
@app.post("/readfile/")
async def read_file(file: UploadFile):
    contents = file.file.read()
```
여러개의 파일을 받기 위해서는 list로 감싸주어야합니다.

```python
async def create_file(files: list[bytes] = File()):
    ...

async def upload_file(files: list[UploadFile]):
    ...
```
`File`과 `Form`을 함께 사용하여 선언할 수 있습니다.  
하지만 요청의 `body`가 `multipart/form-data`의 http요청을 받기 때문에 `Body`파라미터는 사용할 수 없습니다.  

## Error Handling
HTTPException 이용해서 raise를 발생시켜 에러를 일으킬 수 있습니다.
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```
응답으로는 `404`,`{"detail": "Item not found"}`을 받습니다.  
`headers`파라미터를 통해 `dict`에 응답 헤더를 추가할 수 있습니다.  
app에 exceprion_handler를 통해서 error처리를 등록하는 방법이 있습니다.  
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```
하지만 app에 직접 등록하고 따로 관리하기 힘든 부분이 보여 차후에 error를 따로 관리 할 수 있는 방법을 찾아 정리하겠습니다.  

## Path Operation Configuration
### Response Status Code
엔드 포인트에 `status_code` 키워드를 이용해서 상태코드를 반환할 수 있습니다.  
상태 코드는 `fastapi.status`와 `starlette.status` 모두 사용 가능합니다.  
```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```
### Tags
엔드포인트에 tags를 추가하여 분류할 수 있습니다.
tags를 추가하는 위치는 세 곳에 위치해 있습니다.
1. include_router
2. APIRouter
3. router.method

세곳에 다른 tags로 설정할 경우 해당 엔드포인트는 docs에서 여러개 존재 할 수 있습니다.  
또한 Enum을 통해서 클래스로 정의하여 사용할 수 있습니다.
```python
from enum import Enum

class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags.items])
def func():
    ...
```
### Summary and description
엔드포인트에 대한 설명을 `summary`와 `description`옵션으로 추가할 수 있습니다.  
```python
@app.post(
    "/items/",
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item):
    return item
```
`summary`가 없을 경우 기본값은 함수명이 입력됩니다.  
`description`은 docstring으로 대체할 수 있습니다.  
설명이 여러 줄이고 복잡할 경우 docstring을 추천합니다. 또한, Markdown형식으로 입력할 수 있습니다.  
### Response description
`response_description`을 이용해서 응답에 대한 설명을 추가할 수 있습니다.  
기본 값은 fastapi가 자동적으로 성공적인 응답 중 하나를 표시합니다.
```python
@app.post(
    "/items/",
    summary="Create an item",
    response_description="The created item"
)
async def create_item(item):
    return item
```
### Deprecate a path operation
사용하지 않는 엔드포인트는 별도로 표시를 하거나 완전 삭제하는 것이 좋습니다.  
`deprecated`를 사용하여 사용하지 않는다고 표시 할 수 있지만,
docs를 통해서 요청 테스트는 진행 할 수 있습니다.  

## JSON Compatible Encoder
`jsonable_encoder`함수를 이용해서 pydantic 모델로 전달받은 파라미터를 `dict`형태로 변환할 수 있습니다.  
이를 이용해서 DB에 저장하거나 `json.dumps()`로 인코딩하여 별도의 처리를 할 수 있습니다.

## Body - Updates
### HTTP PUT Method
`PUT`을 이용하여 데이터를 수정할 수 있습니다.  
이 과정에서 pydantic 모델의 내용을 위의 `jsonable_encoder`를 이용해서 `dict` 형식으로 변환하면 파라미터 처리가 용이합니다.  
```python
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Item(BaseModel):
    ...

@app.put('/update/')
async def update_item(item: Item):
    update_datas = jsonable_encoder(item)
    updated_item = Item(**update_datas)
    updated_item.save()
    return update_item
```
### HTTP PATCH Method
`PATCH`를 이용하여 부분적으로 데이터를 수정할 수 있습니다.  
방법은 위의 `PUT`과 유사하지만 수정이 필요한 데이터만 부분적으로 변경해야합니다.  
pydantic 모델에서 존재하는 필드만 가져오는 `exclude_unset`을 사용합니다.  
`exclude_unset`에 대한 설명은 [response model - parameter](#response-model)의 `Parameter로 출력 데이터 선택`를 참고하면 좋을 것입니다.  
```python
from pydantic import BaseModel

class Item(BaseModel):
    ...

@router.patch('/little_update/{item_id}')
async def little_update(item_id: int, item: Item):
    update_datas = item.dict(exclude_unset=True)
    # update db
    origin_item = db.get(item_id)
    origin_item.update(**update_datas)
    return origin_item
    
```

### Pydantic model's update parameter
pydantic model `.copy()` 함수의 파라미터로 `update`를 사용하여 데이터를 수정할 수 있습니다.  
공식문서에서는 이렇게 데이터를 수정할 수 있다고 하지만 DB를 수정해야할 경우에는 ORM을 이용해서 수정하는 것이 안전할 것으로 예상됩니다.

또한, 부분 업데이트를 수행할 경우 추가 pydantic model(ex. ItemUpdate)을 선언하여 기본값을 지정하여주는것이 좋습니다.  

## Dependencies
### Dependency Injection
의존성 주입은 프로그래밍에서 코드가 작동하는데 필요한 항목을 선언하는 방법입니다.  
의존성 주입은 다음의 경우에 유용합니다.
* 논리를 공유
* 데이터베이스 공유
* 보안, 인증, 역할 요구사항 시행
```python
async def depends_injection(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
```
각 파라미터에 자료형이 지정되어 있고, 기본값이 설정되어 있습니다.  
이것이 종속성(Dependency)을 부여한 것입니다.  
### Depends
`Depends`함수를 임포트 하여 엔드포인트의 기본값으로 선언하면 의존성 주입이 됩니다.  
```python
from fastapi import Depends, FastAPI

app = FastAPI()


async def depends_injection(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(depends_injection)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(depends_injection)):
    return commons
```
Depends의 파라미터로는 단일 함수만 전달합니다.  
위 예에서는 아래의 요청을 통해서 정상적으로 Depends의 함수에 파라미터가 입력되어 응답을 받는 것을 확인 할 수 있습니다.  
```bash
curl -X 'GET' 'http://127.0.0.1:8000/items/?q=qw&skip=1&limit=12' \
    -H 'accept: application/json'
```
이 의존성을 이용하여 코드의 재사용성을 향상 시킬수 있습니다.  
또한, `async def`와 `def` 두 함수 선언을 모두 사용할 수 있습니다.  

계층적 종속성 주입이 가능하고, 모든 각 계층별 종속성을 만족한 후에 각 단계에서 결과를 반환합니다.  

### Classes as Dependencies
위에서는 함수를 이용해서 종속성을 주입하였습니다.  
함수 대신에 클래스를 이용해서 종속성을 주입할 수 있습니다.
```python
from fastapi import Depends, FastAPI

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
```
클래스를 이용하여 종속성을 주입하려면 클래스의 **생성자(\_\_init\_\_)** 정의에 유의해야합니다.  

클래스를 이용해서 종속성을 주입하는 방법은 여러가지가 있습니다.

```python
# 1.
async def read_items(commons=Depends(CommonQueryParams)):
    pass
# 2.
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    pass
# 3.
async def read_items(commons: CommonQueryParams = Depends()):
    pass
```
1, 2, 3번 방법 모두 종속성을 주입하는 방법이고 FastAPI가 이해할 수 있습니다.  
하지만 1번의 경우 파라미터의 타입정의가 없습니다.  
2번의 경우 클래스를 중복으로 작성되어있습니다.  
1번과 2번의 방법보다 3번의 방법을 이용하는 것이 유용합니다.  
3번은 파라미터의 타입정의가 되어있고 `Depends()`는 `Depends(CommonQueryParams)`과 같은 의미를 내포하고 있습니다.  

종속성을 클래스로 정의하는 것은 생성자를 통해 새로운 인스턴스를 생성하는 것이기 때문에 사용에 유의해야할 것으로 예상합니다.  

### Sub-dependencies
하위 종속성을 정의할 수 있습니다.  
종속성에 종속성을 부여하는 관계를 정의하여 하위 종속성을 구현할 수 있습니다.  
```python
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: str = Cookie(default=None)
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
```
엔드포인트에서 종속성이 주입되고 해당 종속함수에서 또다른 종속성이 주입되어 있습니다.  
이렇게 간단하게 하위 종속을 주입할 수 있고 사용할 수 있습니다.  
또한 **동일한 종속을 여러번 사용**해야할 경우 캐시에 저장합니다.  
캐시에 저장하지 않으려면 `Depends()`에 `use_cache`를 `False`로 설정해야합니다.  

### Dependencies in path operation decorators
종속성을 path 정의와 함께 선언할 수 있습니다.  
path에서 함께 선언하는 경우 함수의 반환 값은 사용할 수 없지만, 함수의 내부 블록을 실행합니다.

```python
from fastapi import Depends


def func1(q: str):
    ...

def func2(id: int):
    ...

@app.get("/items/", dependencies=[Depends(func1), Depends(func2)])
async def func():
    ...
```
path 종속성도 인수의 요구사항을 충족해야하며 내부에서 에러를 발생시킬수 있습니다.  
return 값이 있어도 반환 값을 사용하지 않습니다.  
이를 이용해서 다른 함수를 종속하여 사용할 수 있습니다.  
### Global Dependencies
일부 프로그램에서는 app 전체에 종속성을 부여해야할 필요가 있습니다.  
fastapi에서는 프로그램 전체에도 종속성을 주입할 수 있습니다.
```python
from fastapi import Depends, FastAPI

async def depend_func1():
    pass

async def depend_func2():
    pass

app = FastAPI(dependencies=[Depends(depend_func1), Depends(depend_func2)])
```
app전체 프로그램에 의존성을 주입하는 것과 미들웨어를 추가하는 것에 대해서는 확인이 필요해보입니다.  

### Dependencies with yield
`yield`를 이용해서 종속 완료후 처리 단계를 추가할 수 있습니다.  
공식문서에서는 DB Session에 대해 설명되어 있고 이 종속성은 많이 사용되어 중요하다고 생각합니다.  
```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```
종속성 주입으로 `yield`의 값이 반환값이 경로(path operation)에서 사용되고,
경로의 작업이 완료(응답의 전달)되면 `finally`를 이용해서 이후 처리를 진행합니다.  
`try`문을 사용하여 종속성을 사용하는 동안에 발생하는 모든 예외를 받을 수 있습니다.  
그리고 예외가 발생하여도 `finally`를 이용하여 종속성을 안전하게 마무리할 수 있습니다.  
또한, 하위 종속에 `yield`를 사용할 수 있습니다. 아래의 예시 코드를 첨부하였습니다.  
```python
from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
```
`yield`와 `return`은 필요에 따라 사용할 수 있으며, `async def`와 `def`도 필요에 따라 선택할 수 있습니다.  

#### `HTTPException`을 사용할 경우 주의해야할 사항이 있습니다.  
`HTTPException`을 이용해서 응답을 보낼 경우에는 `yield`가 작동하지 않을 수 있습니다.  
**Exception Handlers**는 계속 실행 중이고, 응답 코드를 전송한 후에 `yield`가 실행되어 종료되지 않을 수 있습니다.  
따라서 `yield`이후에 `HTTPException`예외가 발생하면 기본 예외 또는 사용자 예외를 통해 처리하고 400 응답코드를 전송해야합니다.  

#### `with`구문을 통해서 같은 `yield`를 수행할 수 있습니다.  
```python
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
```
클래스의 `__enter__`와 `__exit__`을 이용하여 `yield`의 실행과 종료를 수행할 수 있습니다.  

## Security
fastapi는 security를 통해 보안에 대해 정의할 수 있습니다.  
이를 통해서 보안, 인증, 권한처리를 구현할 것이고 `OAuth2`, `OpenAPI`, `JWT`에 대해서 서술할 것입니다.  

### Security First Steps
보안을 위해서 `Authorize` 인증을 수행합니다.  
```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```
`bearer`토큰을 사용하기 위해 `OAuth2PasswordBearer`의 이용해서 종속성을 주입하면 `Authorize`를 수행해야합니다.  
인증을 위해서는 유저가 있는지 확인해야하고 유저를 검증해야합니다.

유저확인을 위해 토큰으로 유저를 확인하는 코드이지만, 이번에는 유저를 생성하고 그 응답을 받습니다.  
```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```
이제 token을 받아오는 엔드포인트를 작성해야 합니다.  
```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/token/")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "bearer"}
```
`fastapi.security`에서 `OAuth2PasswordRequestForm`클래스를 종속성으로 주입합니다.  
`OAuth2PasswordRequestForm`의 매개변수로는 아래의 항목이 있습니다.  
* `username` : 필수요소.
* `password` : 필수요소.
* `scope` : 선택요소.
* `grant_type` : 선택요소.
* `client_id` : 선택요소.
* `client_secret` : 선택요소.
 
_`grant_type`은 OAuth2의 spec에 요구되지만 `OAuth2PasswordRequestForm`에서는 선택사항입니다.  
만약 필수요소로 추가하고 싶다면 `OAuth2PasswordRequestFormStrict`을 사용하면 됩니다._  

그리고 그 데이터를 처리하여야 하지만 이번에는 유저이름을 토큰으로 반환합니다.  
응답으로는 `access_token`과 `token_type`을 가지고 있어야하며 `JSON`타입이어야 합니다.  

필요한 경우 `OAuth2PasswordRequestForm`대신에 `Form`파라미터를 이용해서 직접 정의하여 사용할 수 있습니다.
> ```python
> async def get_current_user(token: str = Depends(oauth2_scheme)):
>     user = fake_decode_token(token)
>     if not user:
>         raise HTTPException(
>             status_code=status.HTTP_401_UNAUTHORIZED,
>             detail="Invalid authentication credentials",
>             headers={"WWW-Authenticate": "Bearer"},
>         )
>     return user
> ```
> 401 "UNAUTHORIZED" status code에는 헤더에 `WWW-Authenticate`항목을 추가하는 것이 좋습니다.  
> 이것은 표준 사용법에 의한 것으로 미래의 나 또는 다른 개발자가 사용할 수 있습니다.

### OAuth2 with Password (and hashing), Bearer with JWT tokens
사용자를 저장할 때에는 비밀번호를 암호화하여 저장해야합니다.  
암호화를 하기 위한 라이브러리를 설치합니다.  
```bash
$ pip install "passlib[bcrypt]"
```
`CryptContext`클래스를 이용해서 비밀번호를 암호화 합니다.  
```python
from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


class User(BaseModel):
    username: str
    email: str  = None
    full_name: str = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str
```
`CryptContext`를 이용해서 암호를 Hash로 변환하고 검증할 수 있습니다.  
그리고 유저가 입력한 비밀번호와 hash 비밀번호를 확인하여 맞을 경우에만 해당 유저의 데이터를 반환합니다.  

jwt를 이용해서 토큰을 생성하고 유저의 정보를 확인 할 수 있습니다.  
jwt는 세 부분으로 구성되어 있는데 **Header, Payload, Signature**입니다.  
다시 Signature는 Header, Payload, Private Key의 조합으로 구성합니다.  
jwt를 사용하기 위해서는 라이브러리를 설치해야합니다.
```bash
$ pip install "python-jose[cryptography]"
```
jwt는 secret_key, algorithm을 정의하고 이를 조합하여 token을 생성합니다.  
이를 정의하고 절대로 공개되면 안됩니다.  
```python
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
```
여기서는 `$ openssl rand -hex 32`를 통해서 랜덤키를 생성하였습니다.  
```python
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    

fake_users_db = {}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```
`jwt.encode`에 `dict`타입의 데이터와 secret_key, algoritm을 전달하면 token이 생성됩니다.  
이를 전달하고 사용할 때마다 `jwt.decode`를 이용해서 사용자를 확인하면 됩니다.  

## Middleware
미들웨어는 요청이 있을 경우에 실행합니다.  
요청이 들어오는 경우 해당 요청의 함수를 실행하기 전/후로 요청 및 응답에 대한 처리를 수행할 수 있습니다.  
미들웨어를 수행하기 위해서는 `app.middleware`를 사용합니다.
```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```
`call_next`를 이용해서 다음 미들웨어 또는 함수로 실행을 진행 할 수 있고,  
결과 값이 `response`로 전달되어 응답에 대한 처리를 수행할 수 있습니다.  
또한 사용자 정의 클래스를 이용해서 middleware를 구성할 수 있습니다.  
```python
from starlette.datastructures import URL, Headers
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import FastAPI

class MiddleWare:
    def __init__(self, app: ASGIApp, params):
        ...

    def __call__(self, scope: Scope, receive: Receive, send: Send):
        ...

app = FastAPI()

app.add_middleware(MiddleWare)
```
위의 형식으로 사용자정의 클래스를 middleware로 정의하여 사용할 수 있습니다.
middleware는 정의된 순서대로 요청이 들어와 처리되고 순서의 반대로 응답이 처리되어 순서에 유의해야합니다.

## CORS (Cross-Origin Resource Sharing)
CORS는 교차 출처 자원 공유로 해석됩니다.  
origin을 통해서 외부에서 서버의 자원을 활용하고 제어하는 허가를 확인합니다.  
`origins`에 등록된 host만 서버의 자원을 활용할 수 있고 부가적으로 `methods`, `headers`, `credentials` 등을 확인 할 수 있습니다.  
fastapi는 라이브러리로 지원해주고 middleware로 설정 가능합니다.
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## SQL (Relational) Databases
fastapi는 `SQLAlchemy`를 이용해서 Database와 연결합니다.  
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```
engine을 통해서 데이터베이스와 연결하고, sessionmaker로 요청마다 연결session을 만들어 데이터를 전송합니다.  
declaratiove_base를 상속받아서 orm model을 생성합니다.  
모델을 생성할 때에는
```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```
declarative_tive의 생성자를 import한 후에 클래스에 상속합니다.  
그리고 `__tablename__`은 DB table 이름입니다.  
각 field의 이름을 정하고 속성을 정의합니다.
`relationship`은 연관 field로 외래키로 적용되어있는 row를 가질 수 있습니다.  
Database에 테이블을 생성하는 방법은 직접 sql DDL문을 작성하여 생성할 수도 있고 orm을 이용하여 생성할 수 있습니다.  
```python
# models.py
from database import Base  # declarative_base()

# main.py
import models
from database import engine

models.Base.metadata.create_all(bind=engine)
```
declarative_base 객체의 metadata에 create_all을 통해서 테이블을 생성 할 수 있습니다.  

`Alembic`을 이용해서 migration을 진행 할 수 있습니다.  
[Alembic Docs](https://alembic.sqlalchemy.org/en/latest/)공식문서를 통해서 확인하고 사용해야할 것으로 보입니다.  

### DB model to pydantic
DB에서 불러온 데이터를 응답으로 보낼 경우 `response_model`에 pydantic 모델을 정의합니다.  
여기서 pydantic class는 DB모델의 변환을 허용해야합니다.  
```python
from pydantic import BaseModel

class Item(BaseModel):
    field1: str
    field2: int
    
    class Config:
        orm_mode = True
```
pydantic model에 `Config class`를 생성한 후에 `orm_mode`를 `True`로 설정하면 DB데이터를 pydantic모델로 변환 가능합니다.  

## Bigger Applications - Multiple Files
### APIRouter class
엔드포인트를 한 파일에 정의할 경우 유지보수가 어렵습니다.  
그래서 `APIRouter`를 이용해서 엔드포인트 들을 분할 하여 관리할 수 있습니다.  
```python
from fastapi import APIRouter

router = APIRouter(prefix="/sub-path")

@router.post("/path")
async def func():
    return 
```
이미 코드에 이 클래스를 사용하여 나누어 관리하고 있습니다.  
`APIRouter`는 `main:app`에 추가해야 접근이 가능합니다.  
```python
from fastapi import FastAPI
import apirouter

app = FastAPI()
app.include_router('apirouter.router')
```
정의된 router를 import한 후에 `include_router`에 추가합니다.  
`FastAPI`와 `APIRouter`는 모두 `prefix`, `tags`, `dependencies`, `responses`등의 옵션을 지정할 수 있습니다.  

## Background Tasks
클라이언트는 응답을 받기 전에 작업이 완료될 때까지 기다릴 필요가 없는 작업에 유용합니다.  
예를 들어 이메일 알림이나 길고 느린 데이터 처리 같은 작업입니다.  
`BackgroudTasks`를 이용해서 비동기 작업을 수행합니다.
```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```
종속성 주입으로 사용할 경우 경로작업, 종속 함수, 하위 종속함수에서 모두 사용할 수 있습니다.  
`add_task`를 통해 작업을 전달하면 fastapi가 작업을 실행합니다.  
`starlette.background.BackgroundTask`를 이용할 수 있지만 fastapi의 `BackgroundTasks`사용을 권장합니다.  
많은 백그라운드 처리가 필요한 경우 `Celery`사용을 권장합니다.  
celery사용법은 나중에 기술하겠습니다.

## Metadata and Docs URLs
### Metadata
app에 대한 metadata 제목, 설명, 라이센스, 작성자 등을 작성할 수 있습니다.  
app선언에 파라미터로 입력합니다.  
* `title`: str. app 제목.
* `description`: str. app에 대한 설명.
* `version`: str. app 버전.
* `terms_of_service`: url. 서비스 이용약관.
* `contact`: {'name': <str>, 'url': <url>, 'email': <email>}. 작성자 이름 및 정보.
* `license_info`: {'name': <str>, 'url': <url>}. 라이센스 정보.  
```python
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
```

또한, tags에 대한 metadata를 정의할 수 있습니다.
각 tag 별로 설명과 함께 연결된 url을 연결할 수 있습니다.  
설명은 docs의 tags 이름 뒤에 설명이 있고, 오른쪽에 연결 url이 있습니다.  
그리고 정의한 순서대로 docs의 tag 표시 순서가 정해집니다.
```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)
```

### OpenAPI URL
docs의 기본 URL은 `<host>:<port>/openapi.json`입니다.  
``매개변수를 이용해서 openapi주소를 변경할 수 있습니다.  
```python
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/openapi.json")
```
openapi를 json 형식으로 받아올 수 있습니다.  

### Docs, Redoc URL
기본값은 docs는 `/docs`, redoc은 `/redoc`으로 설정되어 있습니다.  
변경하기 위해서는 `docs_url`, `redoc_url`을 이용해 변경합니다.
```python
from fastapi import FastAPI

app = FastAPI(docs_url="/documentation", redoc_url=None)
```

## Testing
테스트를 진행할 때에는 `TestClient`클래스를 이용합니다.
매개변수로 서버의 app을 전달하고 testclient에서 `GET`, `POST` 등의 요청을 보내 응답값으로 테스트를 진행합니다.
```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```
pytest를 통해서 테스트를 진행하는 것을 권장하며 파일과 함수가 `test_`로 시작해야합니다.  
그리고 Method 구현 방식과 Class 구현 방식이 있습니다.  
Method 구현 방식은 위의 방법으로 `test_`로 시작하는 함수를 정의합니다.  

Class 구현 방식은 `Test`로 시작하는 클래스를 정의하고 그 내부에 함수를 정의 할 수 있습니다.  
Class 테스트를 진행하기 전/후로 사전 작업이 필요한 경우 `setup_class(cls)`, `teardown_class(cls)` 클래스 함수를 정의 할 수 있습니다.  
이 두 함수는 `@classmethod`로 데코레이트 해야합니다.
각 함수의 테스트 진행 전/후에도 사전 작업을 수행할 수 있습니다. `setup_method()`, `teardown_method()`를 정의하면 됩니다.  
```python

from fastapi.testclient import TestClient

from main import app

class TestMain:

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    @classmethod
    def teardown_class(cls):
        ...

    def test_read_main(self):
        ...
```

## Debug
디버그는 개발 단계에서 데이터를 확인하기에 좋은 기능입니다.  
작성한 코드의 결과값을 확인 할 수 있고, 에러가 발생한다면 직전까지 실행 후 입력 데이터를 확인 할 수 있습니다.  
fastapi는 editor를 통해서 디버그를 쉽게 작동 할 수 있습니다.  
먼저 서버를 cli가 아닌 editor에서 실행 할 수 있어야합니다.(pycharm은 다른 방법도 있습니다.)

```python
import uvicorn
from fastapi import FastAPI
from uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
`if __name__ == "__main__`을 통해서 파일 실행시 서버를 구동할 수 있게 합니다.  
그리고 이 파일을 `debug`모드로 실행하면 됩니다.  
원하는 위치에 브레이크포인트(빨간점)을 설정하고 Swagger, curl, postman 등을 통해 요청을 보내면 됩니다.  

> pycharm에서는 `run/debug configuration`을 통해서 debug 및 run을 할 수 있습니다.  
> 1. `+버튼(add new configuration)`을 누르고 `FastAPI`를 선택합니다.
> 2. `Application file`을 FastAPI 클래스를 정의한 파일로 설정합니다.
> 3. `Uvicorn options`에 필요한 옵션을 추가합니다.  
> 
> 이 방법으로 파일에 코드 입력 없이 실행 가능합니다.
> 만약 배포를 cli로 실행할 경우에는 이 방법이 효율적일 수 있습니다.
