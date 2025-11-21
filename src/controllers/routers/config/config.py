from fastapi import APIRouter, Request
from fastapi.params import Depends

from src.domain.entities import Application


class RouterConfig:
    _app_prefix: str = '/{app_id}'
    _tenant_prefix: str = _app_prefix + '/t/{tenant_token}'

    @staticmethod
    def get_unprotected_router() -> APIRouter:
        return APIRouter(prefix=RouterConfig._app_prefix, dependencies=[Depends(RouterConfig.load_app_path_param)])

    @staticmethod
    def get_private_router() -> APIRouter:
        return APIRouter(prefix=RouterConfig._tenant_prefix, dependencies=[Depends(RouterConfig.load_app_path_param), Depends(RouterConfig.load_tenant_path_param)])

    @staticmethod
    async def load_app_path_param(request: Request, app_id: str):
        request.state.application = Application.from_value(app_id)

    @staticmethod
    async def load_tenant_path_param(request: Request, tenant_token: str):
        request.state.tenant_token = tenant_token
