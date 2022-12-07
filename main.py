from enum import Enum

import uvicorn
from fastapi import FastAPI

from routers import (
    body,
    path_parameter,
    query_parameter,
    cookie,
    headers,
    response,
    form,
    errors_handling,
    path_operation_conf,
    encode_json,
    update,
)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(body.router, tags=['body'])
app.include_router(path_parameter.router, tags=['path_parameter'])
app.include_router(query_parameter.router, tags=['query_parameter'])
app.include_router(cookie.router, tags=['cookie'])
app.include_router(headers.router, tags=['headers'])
app.include_router(response.router, tags=['response'])
app.include_router(form.router, tags=['form'])
app.include_router(errors_handling.router, tags=['error'])
app.include_router(path_operation_conf.router, tags=['path_oper_conf'])
app.include_router(encode_json.router, tags=['encode_json'])
app.include_router(update.router, tags=['update_db'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)








