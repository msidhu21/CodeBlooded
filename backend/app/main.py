# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api import auth, items, profile, admin, export, external

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="COSC310 backend", version="M3")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.router)
    app.include_router(items.router)
    app.include_router(profile.router)
    app.include_router(admin.router)
    app.include_router(export.router)
    app.include_router(external.router)
    return app

# global for dev server
app = create_app()
