from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from ..models.dto import ProfileUpdate, AuthUser
from ..services.profile_service import ProfileService
from ..core.db import get_db

router = APIRouter(prefix="/profile", tags=["profile"])

@router.patch("", response_model=AuthUser)
def update_profile(req: ProfileUpdate,
                   authorization: str | None = Header(default=None),
                   db: Session = Depends(get_db)):
    user_id = 1
    return ProfileService(db).update(user_id, req)

