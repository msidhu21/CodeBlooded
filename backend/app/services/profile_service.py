from typing import Dict, Any
from ..repos.user_repo import UserRepo
from ..models.dto import ProfileUpdate, AuthUser

class ProfileService:
    def __init__(self):
        self.repo = UserRepo()

    def update(self, user_id: int, req: ProfileUpdate) -> AuthUser:
        """Apply partial updates (name, picture, contact) and return AuthUser."""
        contact_dict: Dict[str, Any] | None = None
        if req.contact is not None:
            contact_dict = req.contact.dict()

        updated = self.repo.update_profile(
            user_id,
            name=req.name,
            picture=req.picture,
            contact=contact_dict,
        )
        return AuthUser.model_validate(updated)
