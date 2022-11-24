from fastapi import APIRouter, Form, File, UploadFile

router = APIRouter(
    prefix='form'
)

@router.post('/login/')
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

@router.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"file": file.filename}


@router.post("/readfile/")
async def read_file(file: UploadFile):
    contexts = file.file.read()
    return {"file": file.filename}
