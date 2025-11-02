import uvicorn
from fastapi import FastAPI

from src.controllers.routers import participant_controller, category_controller, event_controller

app = FastAPI()

app.include_router(
    participant_controller.router,
    tags=["participants"],
)

app.include_router(
    category_controller.router,
    tags=["categories"],
)

app.include_router(
    event_controller.router,
    tags=["events"],
)



@app.get('/')
async def root():
    return {'message': 'Server is running. This is the root path.'}


def run_server():
    uvicorn.run(app, host='0.0.0.0', port=8000)
