from typing import List

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import PlatformTenantTokens, TenantLookupToken, Application, UserRole
from src.domain.interfaces import TenantLookupTokenDataProvider
from src.services.postgres.models.token import TokenModel
from src.services.postgres.pg_base import PgBase


class TokenDataProvider(PgBase, TenantLookupTokenDataProvider):

    async def create_platform_tokens(self, tokens: PlatformTenantTokens) -> PlatformTenantTokens:
        session: AsyncSession
        async with self._setup_connection() as session:
            admin_token_model: TokenModel = TokenModel.from_entity(tokens.AdminToken)
            editor_token_model: TokenModel = TokenModel.from_entity(tokens.EditorToken)
            visitor_token_model: TokenModel = TokenModel.from_entity(tokens.VisitorToken)
            session.add(admin_token_model)
            session.add(editor_token_model)
            session.add(visitor_token_model)
            await session.commit()
            await session.refresh(admin_token_model)
            await session.refresh(editor_token_model)
            await session.refresh(visitor_token_model)
            ptt = PlatformTenantTokens(
                AdminToken=admin_token_model.to_entity(),
                EditorToken=editor_token_model.to_entity(),
                VisitorToken=visitor_token_model.to_entity(),
                TenantId=admin_token_model.tenant_id,
            )
            return ptt

    async def get_platform_tokens(self, lookup_token: TenantLookupToken) -> PlatformTenantTokens:
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = select(TokenModel)\
                .where(TokenModel.tenant_id.is_(lookup_token.tenant_id))\
                .where(TokenModel.application.is_(lookup_token.app.value))
            res: ScalarResult[TokenModel] = await session.scalars(stmt)
            models: List[TokenModel] = list(res.all())
            if len(models) != 3:
                raise ValueError(f'expected three tokens for tenant id {lookup_token.tenant_id}, got {len(models)}')

            d = {model.role: model for model in models}
            if set(d.keys()) != {UserRole.ADMIN.value, UserRole.EDITOR.value, UserRole.VISITOR.value}:
                raise ValueError(f'invalid set of roles for tenant id {lookup_token.tenant_id}, got "{', '.join(d.keys())}"')

            p = PlatformTenantTokens(
                AdminToken=TokenModel.to_entity(d.get(UserRole.ADMIN.value)),
                EditorToken=TokenModel.to_entity(d.get(UserRole.EDITOR.value)),
                VisitorToken=TokenModel.to_entity(d.get(UserRole.VISITOR.value)),
                TenantId=lookup_token.tenant_id,
            )
            return p