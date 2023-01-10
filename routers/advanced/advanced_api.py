from fastapi import APIRouter
from fastapi.routing import APIRoute

from routers.advanced.endpoint import operation_config, status_code, direct_response, add_response_openapi, cookies,\
    headers

router = APIRouter(
    prefix="/advanced"
)

router.include_router(operation_config.router, tags=["path_operation_config"])
router.include_router(status_code.router, tags=["status code"])
router.include_router(direct_response.router, tags=["direct_response"])
router.include_router(add_response_openapi.router, tags=["add_openapi_response"])
router.include_router(cookies.router, tags=["cookies"])
router.include_router(headers.router, tags=["headers"])


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