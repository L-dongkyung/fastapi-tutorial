from enum import Enum

import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 경로의  변수와 함수의 파라미터 이름이 같아야합니다. 다르면 에러 발생.
@app.get("/items/{item_id}")
async  def read_item(item_id):
    """
    query string으로 인수를 받아서 처리 \n
    :url: server.com/items/item_id
    :param item_id:
    :return:
    """
    return {"item_id": item_id}

# 경로에 중접이 될 경우 위에서 부터 인식합니다.
# 아래의 두 경로 위치가 바뀔 경우 users/me 경로는 실행 할 수 없습니다.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# 이 함수는 호출 할 수 없습니다. 위의 read_user에서 모두 실행합니다.
# 그러므로 경로를 정의 할때에 주의 해야합니다.
@app.get("/users/{user_name}")
async def read_user_name(user_name: str):
    return {"user_name": user_name}


class ModelName(str, Enum):
    """
    str을 상속하는 이유는 경로의 인수가 str형이라는 것을 알려줘 렌더링 할 수 있게 해줍니다.
    Enum을 통해서 swagger에서 파라미터 설정을 선택할 수 있습니다.
    """
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# 파일 path 매개변수 사용
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    /로 시작하는 파일의 경로를 받을 수 있습니다.
    url에는 이중 슬래시 // 가 입력됩니다.
    :param file_path: /로 시작하는 경로.
    :return:
    """
    return {"file_path": file_path}


# 쿼리 매개변수
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


# 쿼리파라미터 선택적 입력.
from typing import Union
@app.get("/items_q/{item_id}")
async def read_item_q(item_id: str, q: Union[str, None] = None):
    if q:
        return {'item_id': item_id, 'q': q}
    return {'item_id': item_id}


# bool자료형의 입력.
# bool형으로는 [1, 0, on, off, True, true, False, false, yes, no]을 받을 수 있습니다.
@app.get("/short/{short_id}")
async def short(short_id: str, short: bool = False):
    item = {'short_id': short_id}
    if not short:
        item.update({"desc": "This is an amazing item that has a long disc"})
    return item


# 필수 쿼리 매개변수
@app.get("/req_short/{short_id}")
async def short_req(short_id: str, needy: str):
    return {"short_id": short_id, "needy": needy}


# 선택으로 논값?
@app.get("/option_short/{short_id}")
async def opt_short(short_id: str, option: Union[int, None] = None):  # Union을 사용하는 것과 안쓰는 것의 차이는?
    return {'short_id': short_id, 'option': option}


# request body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/create_items/")
async def create_item(item: Item):
    return item
