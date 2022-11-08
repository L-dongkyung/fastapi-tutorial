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
