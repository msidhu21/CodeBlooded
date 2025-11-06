from fastapi import APIRouter, Header
from ..models.dto import ProfileUpdate, AuthUser
from ..services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])

@router.patch("", response_model=AuthUser)
def update_profile(req: ProfileUpdate, authorization: str | None = Header(default=None)):
    user_id = 1  # In a real app, extract from JWT token
    return ProfileService().update(user_id, req)

