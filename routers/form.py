from fastapi import APIRouter, Form

router = APIRouter(
    prefix='form'
)

@router.post('/login/')
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}