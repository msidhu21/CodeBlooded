from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.dto import RegisterRequest, LoginRequest, AuthUser
from ..services.auth_service import AuthService
from ..core.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthUser, status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register(req)

@router.post("/login", response_model=AuthUser)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(req)

@router.get("/me", response_model=AuthUser)
def me_demo():
    return AuthUser(id=1, email="demo@cosc310.ca", name="Demo", role="admin")

