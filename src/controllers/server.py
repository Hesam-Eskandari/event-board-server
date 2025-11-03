import uvicorn
from fastapi import FastAPI

from src.controllers.routers import participant_controller, category_controller, event_controller
from src.library import singleton


@singleton
class Server:
    def __init__(self):
        self._app = FastAPI()

    def run(self):
        self._app.include_router(
            participant_controller.router,
            tags=["participants"],
        )

        self._app.include_router(
            category_controller.router,
            tags=["categories"],
        )

        self._app.include_router(
            event_controller.router,
            tags=["events"],
        )
        uvicorn.run(self._app, host='0.0.0.0', port=8000)
