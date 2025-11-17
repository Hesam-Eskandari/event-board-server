from src.controllers.dtos.base import BaseDTO


class TenantTokenReadDTO(BaseDTO):
    adminToken: str
    editorToken: str
    visitorToken: str
