from abc import ABC

from src.domain.entities import PlatformTenantTokens, TenantLookupToken


class TenantLookupTokenDataProvider(ABC):
    async def create_platform_tokens(self, tokens: PlatformTenantTokens) -> PlatformTenantTokens:
        raise NotImplementedError('[create_platform_tokens] not implemented')

    async def get_platform_tokens(self, lookup_token: TenantLookupToken) -> PlatformTenantTokens:
        raise NotImplementedError('[get_platform_tokens] not implemented')
