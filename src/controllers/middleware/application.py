from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.domain.entities import Application


class ApplicationMiddleware(BaseHTTPMiddleware):
    _application = Application.EventBoard

    async def dispatch(self, request, call_next):
        application = request.state.application
        if application != self._application:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this request cannot be consumed by this application')
        return await call_next(request)