import time
from typing import Callable

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


router = APIRouter(
    prefix="/timed"
)


@router.get("/")
async def not_timed():
    return {"message": "Not timed"}


router.route_class = TimedRoute


@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}

