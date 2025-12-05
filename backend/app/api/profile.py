# app/api/profile.py
from fastapi import APIRouter, Header, HTTPException
from ..models.dto import ProfileUpdate, AuthUser
from ..services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])

# TEMP – always return user 1
@router.get("", response_model=AuthUser)
def get_me(authorization: str | None = Header(default=None)):
    return ProfileService().get(1)

@router.patch("", response_model=AuthUser)
def update_me(
    req: ProfileUpdate,
    authorization: str | None = Header(default=None),
):
    # TEMP – always update user 1
    updated = ProfileService().update(1, req)
    return updated

@router.get("/{user_id}", response_model=AuthUser)
def get_profile(user_id: int, authorization: str | None = Header(default=None)):
    return ProfileService().get(user_id)

@router.patch("/{user_id}", response_model=AuthUser)
def update_profile(
    user_id: int,
    req: ProfileUpdate,
    authorization: str | None = Header(default=None),
):
    updated = ProfileService().update(user_id, req)
    return updated
