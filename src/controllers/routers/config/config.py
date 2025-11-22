from fastapi import APIRouter, Request, Query, Depends, HTTPException, status

from src.domain.entities import Application, TenantLookupToken
from src.domain.interactors import TenantInteractor
from src.services.postgres.pg_token_data_provider import PgTokenDataProvider


class RouterConfig:
    _prefix: str = '/{app_id}'
    _application = Application.EventBoard

    @staticmethod
    def get_unprotected_router() -> APIRouter:
        return APIRouter(prefix=RouterConfig._prefix, dependencies=[Depends(RouterConfig.load_app_path_param)])

    @staticmethod
    def get_private_router() -> APIRouter:
        return APIRouter(prefix=RouterConfig._prefix, dependencies=[Depends(RouterConfig.load_app_path_param), Depends(RouterConfig.load_tenant_path_param)])

    @staticmethod
    async def load_app_path_param(request: Request, app_id: str):
        if app_id != RouterConfig._application.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this request cannot be consumed by this application')
        request.state.application = Application.from_value(app_id)

    @staticmethod
    async def load_tenant_path_param(request: Request, token: str = Query(..., alias="token")):
        if token is None or not token.strip():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no tenant provided")
        interactor = TenantInteractor(PgTokenDataProvider())
        try:
            tenant_token: TenantLookupToken = await interactor.verify_token_and_decode(token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="failed to verify tenant token")
        request.state.tenant_token = tenant_token
