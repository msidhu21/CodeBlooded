from fastapi import APIRouter
from ..models.dto import RegisterRequest, LoginRequest, AuthUser
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthUser, status_code=201)
def register(req: RegisterRequest):
    return AuthService().register(req)

@router.post("/login", response_model=AuthUser)
def login(req: LoginRequest):
    return AuthService().login(req)

@router.get("/me", response_model=AuthUser)
def me_demo():
    return AuthUser(id=1, email="demo@cosc310.ca", name="Demo", role="admin")

