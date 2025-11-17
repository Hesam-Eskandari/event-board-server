from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.domain.entities import TenantLookupToken
from src.domain.interactors import TenantInteractor


class TenantMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        tenant_token: str | None = request.state.tenant_token
        if tenant_token is None:
            if request.method == 'POST' and "/tokens/" in request.url.path:
                pass
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no tenant provided")
        else:
            interactor = TenantInteractor()
            try:
                tenant_lookup_token: TenantLookupToken = await interactor.verify_token_and_decode(tenant_token)
            except Exception:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="failed to verify tenant token")
            request.state.tenant_lookup_token = tenant_lookup_token
        response = await call_next(request)
        return response
