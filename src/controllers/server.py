import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.controllers.routers import participant_controller, category_controller, event_controller
from src.library import singleton


@singleton
class Server:
    def __init__(self):
        self._app = FastAPI()
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # or specify allowed origins
            allow_credentials=True,
            allow_methods=["*"],  # includes OPTIONS automatically
            allow_headers=["*"],
        )

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
