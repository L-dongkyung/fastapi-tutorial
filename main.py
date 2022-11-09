from enum import Enum

import uvicorn
from fastapi import FastAPI

from routers import body, path_parameter, query_parameter

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(body.router)
app.include_router(path_parameter.router)
app.include_router(query_parameter.router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)








