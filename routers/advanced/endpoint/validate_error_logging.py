from typing import Callable, List

from fastapi import Body, APIRouter, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


router = APIRouter(
    prefix="/validate_error_logging"
)
router.route_class = ValidationErrorLoggingRoute


@router.post("/")
async def sum_numbers(numbers: List[int] = Body()):
    return sum(numbers)
