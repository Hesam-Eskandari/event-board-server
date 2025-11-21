from typing import Dict, Any

import pyseto

from src.domain.entities import TenantLookupToken, PlatformTenantTokens, UserRole
from src.domain.exceptions import InsufficientAccessTokenException
from src.domain.exceptions.lookup_token_exception import LookupTokenException
from src.domain.interfaces import TenantLookupTokenDataProvider
from src.library import singleton, PathHelper


@singleton
class TenantInteractor:
    _pyseto_version: int = 4
    _private_key_path: str = f'{PathHelper.get_root_path()}/keys/private.key'
    _public_key_path: str = f'{PathHelper.get_root_path()}/keys/public.key'

    def __init__(self, data_provider: TenantLookupTokenDataProvider):
        self._private_key = None
        self._public_key = None
        self._data_provider: TenantLookupTokenDataProvider = data_provider

    async def populate_private_key(self):
        if self._private_key is not None:
            return
        try:
            self._private_key = pyseto.Key.new(
                version=self._pyseto_version,
                purpose='public',
                key=open(self._private_key_path, 'rb').read(),
            )
        except OSError:
            raise FileNotFoundError('private key file not found')

    async def populate_public_key(self):
        if self._public_key is not None:
            return
        try:
            self._public_key = pyseto.Key.new(
                version=self._pyseto_version,
                purpose='public',
                key=open(self._public_key_path, 'rb').read(),
            )
        except OSError:
            raise FileNotFoundError('private key file not found')

    async def verify_token_and_decode(self, token: str) -> TenantLookupToken:
        await self.populate_public_key()
        decoded = pyseto.decode(self._public_key, token)
        payload: Dict[str, Any] = decoded.payload
        return TenantLookupToken.from_dict(payload)

    async def encode_token(self, token: TenantLookupToken) -> str:
        await self.populate_private_key()
        payload: Dict[str, Any] = token.to_dict()
        return pyseto.encode(self._private_key, payload).decode("utf-8")

    async def generate_lookup_tokens_v1(self) -> PlatformTenantTokens:
        tokens = PlatformTenantTokens.generate()
        await self._data_provider.create_platform_tokens(tokens)
        return tokens

    async def get_lookup_tokens(self, token: str) -> PlatformTenantTokens:
        lookup_token = await self.verify_token_and_decode(token)
        if lookup_token.role != UserRole.ADMIN:
            raise InsufficientAccessTokenException('insufficient permission')
        return await self._data_provider.get_platform_tokens(lookup_token)
