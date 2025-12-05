from ..repos.user_repo import UserRepo
from ..models.dto import ProfileUpdate, AuthUser

class ProfileService:
    def __init__(self):
        self.repo = UserRepo()

    def get(self, user_id: int) -> AuthUser:
        user = self.repo.by_id(user_id)
        return AuthUser(**user)

    def update(self, user_id: int, req: ProfileUpdate) -> AuthUser:
        updated = self.repo.update_profile(
            user_id,
            name=req.name,
            email=req.email,
            role=req.role,
            picture=req.picture,
            contact_email=req.contact_email,
            contact_phone=req.contact_phone,
            location=req.location,
        )
        return AuthUser(**updated)
