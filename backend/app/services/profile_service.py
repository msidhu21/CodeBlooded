from __future__ import annotations

from ..repos.user_repo import UserRepo
from ..models.dto import ProfileUpdate, ContactInfo, AuthUser


class ProfileService:
    def __init__(self, repo: UserRepo | None = None):
        # In real code, this will be the CSV repo.
        # In tests, this gets replaced with StubRepo.
        self.repo = repo or UserRepo()

    def get(self, user_id: int) -> AuthUser:
        row = self.repo.by_id(user_id)  # dict from CSV repo
        return AuthUser(
            user_id=row.get("user_id"),
            email=row.get("email"),
            name=row.get("name"),
            role=row.get("role"),
        )

    def update(self, user_id: int, req: ProfileUpdate) -> AuthUser:
        name = getattr(req, "name", None)
        picture = getattr(req, "picture", None)
        contact = getattr(req, "contact", None)

        # Convert contact into a dict so StubRepo can do contact.get(...)
        contact_arg = None
        if contact is not None:
            if isinstance(contact, dict):
                contact_arg = contact
            elif hasattr(contact, "dict"):
                contact_arg = contact.dict()
            elif hasattr(contact, "model_dump"):
                contact_arg = contact.model_dump()
            else:
                contact_arg = {
                    "email": getattr(contact, "email", None),
                    "phone": getattr(contact, "phone", None),
                }

        # This matches StubRepo.update_profile(self, user_id, *, name=None, picture=None, contact=None)
        updated = self.repo.update_profile(
            user_id,
            name=name,
            picture=picture,
            contact=contact_arg,
        )

        # StubRepo returns a dict with keys: user_id, email, name, role, picture?, contact_email?, contact_phone?
        # AuthUser only needs these four:
        return AuthUser(
            user_id=updated.get("user_id"),
            email=updated.get("email"),
            name=updated.get("name"),
            role=updated.get("role"),
        )
