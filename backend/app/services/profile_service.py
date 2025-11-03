from sqlalchemy.orm import Session
from ..repos.user_repo import UserRepo
from ..models.dto import ProfileUpdate, AuthUser

class ProfileService:
    def __init__(self, db: Session):
        self.repo = UserRepo(db)

    def update(self, user_id: int, req: ProfileUpdate) -> AuthUser:
        u = self.repo.update_profile(user_id, name=req.name)
        return AuthUser.model_validate(u)

