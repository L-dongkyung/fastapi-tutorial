import time

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from routers.tutorial import tutorial_api
from routers.advanced import advanced_api
from routers.advanced.subapp.main import app as subapi

# app info
app_info = {
    "title": "FastAPI Tutorial",
    "description": "tiangolo's Fastapi documents tutorial",
    "version": "0.0.1",
    "contact": {
        "name": "lee dongkyung",
        "email": "ckldk91m@gmail.com"
    },
    "license_info": {"name": "None"}
}

# tags info
tags_info = [
    {"name": "background", "description": "background task tutorial"},
    {
        "name": "depends",
        "description": "dependencies tutorial",
        "externalDocs": {
            "description": "tiangolo docs",
            "url": "https://fastapi.tiangolo.com/ko/tutorial/dependencies/"
        },
    },
]

app = FastAPI(openapi_tags=tags_info, openapi_url="/api/tuto/docs", redoc_url="/tuto/redoc", **app_info)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# tutorials APIs
# app.include_router(tutorial_api.router)

# advanced APIs
app.include_router(advanced_api.router)

# sub application mount
app.mount("/subapi", subapi)

# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)








