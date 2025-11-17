from typing import Any

from sqlalchemy import Column, UUID, String, func, DateTime, Integer

from src.domain.entities import TenantLookupToken, Application, UserRole, TokenType
from src.services.postgres.models import TenantBase


class TokenModel(TenantBase):
    __tablename__ = 'token'
    id = Column(UUID, primary_key=True)
    tenant_id = Column(UUID, nullable=False)
    application = Column(String, nullable=False)
    role = Column(String, nullable=False)
    type = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @staticmethod
    def from_entity(entity: TenantLookupToken) -> 'TokenModel':
        model = TokenModel()
        model.tenant_id = entity.tenant_id
        model.id = entity.id
        model.role = entity.role.value
        model.type = entity.type.value
        model.application = entity.app.value
        model.version = entity.version
        return model

    def to_entity(self) -> TenantLookupToken:
        t = TenantLookupToken()
        t.id = self.id
        t.app = Application.from_value(self.application)
        t.role = UserRole.from_value(self.role)
        t.type = TokenType.from_value(self.type)
        t.version = self.version
        t.tenant_id = self.tenant_id
        return t

    def to_dict(self, exclude_id: bool=False, exclude_fields: list[str] = None) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if not exclude_id or c.name != "id" and c.name not in exclude_fields}
