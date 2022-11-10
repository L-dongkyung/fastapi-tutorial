from enum import Enum

import uvicorn
from fastapi import FastAPI

from routers import body, path_parameter, query_parameter

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(body.router, tags=['body'])
app.include_router(path_parameter.router, tags=['path_parameter'])
app.include_router(query_parameter.router, tags=['query_parameter'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)








