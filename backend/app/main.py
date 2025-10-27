from fastapi import FastAPI
from .api import admin, export

def create_app() -> FastAPI:
    app = FastAPI(title="COSC310 Backend", version="M3")
    app.include_router(admin.router)
    app.include_router(export.router)
    return app

app = create_app()

