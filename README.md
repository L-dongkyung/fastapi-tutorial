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

