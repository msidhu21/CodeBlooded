import pytest
from app.services.profile_service import ProfileService
from app.models.dto import ProfileUpdate, ContactInfo, AuthUser

class StubRepo:
    def __init__(self):
        self.last_args = None
        self.user = {
            "user_id": 1,
            "email": "admin@cosc310.ca",
            "name": "Admin User",
            "role": "admin",
        }

    def update_profile(self, user_id, *, name=None, picture=None, contact=None):
        self.last_args = (user_id, name, picture, contact)
        updated = dict(self.user)
        if name is not None:
            updated["name"] = name
        if picture is not None:
            updated["picture"] = picture
        if contact is not None:
            updated["contact_email"] = contact.get("email")
            updated["contact_phone"] = contact.get("phone")
        return updated

@pytest.fixture
def svc():
    # Bypass __init__ so we don't create a real UserRepo or hit CSV
    s = ProfileService.__new__(ProfileService)
    s.repo = StubRepo()
    return s

def test_update_partial_fields_calls_repo_with_only_those_fields(svc):
    req = ProfileUpdate(name="New Name")
    out = svc.update(1, req)
    assert isinstance(out, AuthUser)
    assert svc.repo.last_args == (1, "New Name", None, None)

def test_update_all_fields_maps_contact_dict(svc):
    req = ProfileUpdate(
        name="Neo",
        picture="p.png",
        contact=ContactInfo(email="a@b.com", phone="555"),
    )
    out = svc.update(1, req)
    assert out.name == "Neo"
    assert svc.repo.last_args == (1, "Neo", "p.png", {"email": "a@b.com", "phone": "555"})
