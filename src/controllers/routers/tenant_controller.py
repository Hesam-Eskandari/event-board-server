from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv

from src.controllers.dtos.tenant import TenantTokenReadDTO
from src.controllers.routers import RouterConfig
from src.domain.exceptions import InsufficientAccessTokenException
from src.domain.interactors import TenantInteractor
from src.services.postgres.pg_token_data_provider import PgTokenDataProvider

public_router = RouterConfig.get_unprotected_router()
private_router = RouterConfig.get_private_router()

@cbv(public_router)
@cbv(private_router)
class TenantController:

    @public_router.post('/tokens/', status_code=status.HTTP_201_CREATED, response_model=TenantTokenReadDTO)
    async def register_tenant(self) -> TenantTokenReadDTO:
        interactor = TenantInteractor(PgTokenDataProvider())
        try:
            p = await interactor.generate_lookup_tokens_v1()
            dto = TenantTokenReadDTO(
                adminToken=await interactor.encode_token(p.AdminToken),
                editorToken=await interactor.encode_token(p.EditorToken),
                visitorToken=await interactor.encode_token(p.VisitorToken)
            )
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"failed generating tokens: {err}")
        return dto

    @private_router.get('/tokens/{token_id}', status_code=status.HTTP_200_OK, response_model=TenantTokenReadDTO)
    async def get_tenant(self, token_id: str) -> TenantTokenReadDTO:
        interactor = TenantInteractor(PgTokenDataProvider())
        try:
            p = await interactor.get_lookup_tokens(token_id)
            dto = TenantTokenReadDTO(
                adminToken=await interactor.encode_token(p.AdminToken),
                editorToken=await interactor.encode_token(p.EditorToken),
                visitorToken=await interactor.encode_token(p.VisitorToken)
            )
        except InsufficientAccessTokenException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="failed fetching tokens")
        return dto
