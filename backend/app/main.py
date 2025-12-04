
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="COSC310 backend", version="M3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, items, profile, admin, export, external

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(profile.router)
app.include_router(admin.router)
app.include_router(export.router)
app.include_router(external.router)