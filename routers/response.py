from typing import Union

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix='/response'
)


class User(BaseModel):
    name: str
    password: str
    email: EmailStr = None
    age: int = 10
    follow: list[str] = None


class UserOut(BaseModel):
    name: str
    email: str = None
    age: Union[int, None] = 10


fake_user_db = {
    "admin": {'name': 'admin', 'password': 'admin', 'email': 'admin@admin.com', 'age': 30, 'follow': ['user1',]},
    "default": {'name': 'default', 'password': 'default', 'email': None, 'age': 10, "follow": None},
    'name': {'name': 'name', "age": None, 'nickname': 'nickname'},
    "user1": {'name': 'user1', 'password': 'user1', 'email': 'user1@admin.com', 'age': 24},
    'user2': {'name': 'user2', 'password': 'user2', 'age': 10}
}


@router.post("/users/", response_model=User, response_model_exclude_unset=True)
async def create_user(user: User):
    return user


@router.get("/user/", response_model=UserOut, response_model_exclude_defaults=True)
async def read_user(user: str):
    return fake_user_db[user]


@router.get("/include_user/", response_model=UserOut, response_model_include={"name", "email"})
async def read_user(user: str):
    return fake_user_db[user]


@router.get("/exclude_user/", response_model=User, response_model_exclude=["password"])
async def read_user(user: str):
    return fake_user_db[user]
