from ..repos.user_repo import UserRepo
from ..core.security import hash_password, verify_password
from ..models.dto import RegisterRequest, LoginRequest, AuthUser
from ..core.errors import Unauthorized

class AuthService:
    def __init__(self):
        self.repo = UserRepo()

    def register(self, req: RegisterRequest) -> AuthUser:
        hashed = hash_password(req.password)
        u = self.repo.create(
            email=req.email,
            password_hash=hashed,
            name=getattr(req, "name", None) or getattr(req, "username", None)
        )
        return AuthUser.model_validate(u)

    def login(self, req: LoginRequest) -> AuthUser:
        u = self.repo.by_email(req.email)
        if not u or not verify_password(req.password, u["password_hash"]):
            raise Unauthorized("Invalid credentials")
        return AuthUser.model_validate(u)


