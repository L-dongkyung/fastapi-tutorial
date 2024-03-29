from fastapi import APIRouter
from fastapi.routing import APIRoute

from routers.advanced.endpoint import operation_config, status_code, direct_response, add_response_openapi, cookies,\
    headers, advanced_depends, oauth2, http_auth, request, dataclass, template, graphql, websocket, gzip, \
    validate_error_logging, time_route
from routers.advanced.endpoint.peewee import main

router = APIRouter(
    prefix="/advanced"
)

router.include_router(operation_config.router, tags=["path_operation_config"])
router.include_router(status_code.router, tags=["status code"])
router.include_router(direct_response.router, tags=["direct_response"])
router.include_router(add_response_openapi.router, tags=["add_openapi_response"])
router.include_router(cookies.router, tags=["cookies"])
router.include_router(headers.router, tags=["headers"])
router.include_router(advanced_depends.router, tags=["advanced-depends"])
router.include_router(oauth2.router, tags=["OAuth2-scopes"])
router.include_router(http_auth.router, tags=["HTTP-Auth"])
router.include_router(request.router, tags=["request"])
router.include_router(dataclass.router, tags=["dataclass"])
router.include_router(main.router, tags=["peewee"])
router.include_router(template.router, tags=["templates"])
router.include_router(graphql.router, tags=["graphql"])
router.include_router(websocket.router, tags=["websocket"])
router.include_router(gzip.router, tags=["gzip_path"])
router.include_router(validate_error_logging.router, tags=["validate_error_logging"])
router.include_router(time_route.router, tags=["timed_route"])


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