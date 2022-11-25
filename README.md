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
