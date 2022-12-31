from fastapi import APIRouter

from routers.tutorial.endpoint import security, errors_handling, encode_json, response, update, path_parameter, \
    query_parameter, debug, background, form, cookie, body, dependencies, path_operation_conf, headers


router = APIRouter(
    prefix="/tutorial"
)

router.include_router(body.router, tags=['body'])
router.include_router(path_parameter.router, tags=['path_parameter'])
router.include_router(query_parameter.router, tags=['query_parameter'])
router.include_router(cookie.router, tags=['cookie'])
router.include_router(headers.router, tags=['headers'])
router.include_router(response.router, tags=['response'])
router.include_router(form.router, tags=['form'])
router.include_router(errors_handling.router, tags=['error'])
router.include_router(path_operation_conf.router, tags=['path_oper_conf'])
router.include_router(encode_json.router, tags=['encode_json'])
router.include_router(update.router, tags=['update_db'])
router.include_router(dependencies.router, tags=['depends'])
router.include_router(security.router, tags=['security'])
router.include_router(background.router, tags=['background'])
router.include_router(debug.router, tags=['debug'])
