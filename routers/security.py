from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter(
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


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


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


