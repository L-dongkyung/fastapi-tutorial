from fastapi import APIRouter
from fastapi.routing import APIRoute

from routers.advanced.endpoint import operation_config, status_code

router = APIRouter(
    prefix="/advanced"
)

router.include_router(operation_config.router, tags=["path_operation_config"])
router.include_router(status_code.router, tags=["status code"])


# def use_route_names_as_operation_ids(router: APIRouter) -> None:
#     """
#     Simplify operation IDs so that generated API clients have simpler function
#     names.
#
#     Should be called only after all routes have been added.
#     """
#     for route in router.routes:
#         if isinstance(route, APIRoute):
#             route.operation_id = route.name  # in this case, 'read_items'
#
#
# use_route_names_as_operation_ids(router)