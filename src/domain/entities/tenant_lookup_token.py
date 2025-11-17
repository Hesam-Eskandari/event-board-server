import enum
import uuid
from typing import Any, Optional, NamedTuple
from uuid import UUID

from src.domain.entities.application import Application
from src.domain.exceptions import LookupTokenException


class UserRole(enum.Enum):
    ADMIN = 'admin'
    EDITOR = 'editor'
    VISITOR = 'visitor'

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_value(val: str) -> Optional['UserRole']:
        return UserRole._value2member_map_.get(val)

class TokenType(enum.Enum):
    TENANT = 'tenant'

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_value(val: str) -> Optional['TokenType']:
        return TokenType._value2member_map_.get(val)


class TenantLookupToken:
    version: int
    type: TokenType
    tenant_id: UUID
    app: Application
    id: UUID
    role: UserRole

    def _validate(self):
        if self.version is None:
            raise LookupTokenException('version is missing in the token')
        if self.type is None:
            raise LookupTokenException('type is missing in the token')
        if self.app is None:
            raise LookupTokenException('app is missing in the token')
        if self.tenant_id is None:
            raise LookupTokenException('tenant_id is missing in the token')
        if self.role is None:
            raise LookupTokenException('role is missing in the token')
        if self.id is None:
            raise LookupTokenException('id is missing in the token')

    def to_dict(self) -> dict[str, Any]:
        self._validate()
        return {
            "v": self.version,
            "k": self.type.__str__(),
            "a": self.app.__str__(),
            "t": self.tenant_id.__str__(),
            "u": self.id.__str__(),
            "r": self.role.__str__(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantLookupToken':
        token = TenantLookupToken()
        token.version = data.get("v")
        token.type = TokenType.from_value(data["k"])
        token.app = Application.from_value(data.get("a"))
        tenant_id = data.get("t")
        token.tenant_id  = UUID(tenant_id) if tenant_id is not None else None
        token_id = data.get("u")
        token.id = UUID(token_id) if token_id is not None else None
        token.role = UserRole.from_value(data.get("r"))
        token._validate()
        return token

    @staticmethod
    def generate(tenant_id: UUID, role: UserRole, app: Application, version: int) -> 'TenantLookupToken':
        token = TenantLookupToken()
        token.id = uuid.uuid7()
        token.tenant_id = tenant_id
        token.app = app
        token.role = role
        token.type = TokenType.TENANT
        token.version = version
        token._validate()
        return token


class PlatformTenantTokens(NamedTuple):
    AdminToken: TenantLookupToken
    EditorToken: TenantLookupToken
    VisitorToken: TenantLookupToken
    TenantId: UUID

    @staticmethod
    def generate(version: int = 1, app: Application = Application.EventBoard) -> 'PlatformTenantTokens':
        tenant_id = uuid.uuid7()
        admin_token = TenantLookupToken.generate(tenant_id, UserRole.ADMIN, app, version)
        editor_token = TenantLookupToken.generate(tenant_id, UserRole.EDITOR, app, version)
        visitor_token = TenantLookupToken.generate(tenant_id, UserRole.VISITOR, app, version)
        return PlatformTenantTokens(admin_token, editor_token, visitor_token, tenant_id)