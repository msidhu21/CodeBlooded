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

    def update_profile(self, user_id, **kwargs):
        self.last_args = (user_id, kwargs)
        updated = dict(self.user)
        # Update any fields that were passed
        for key, value in kwargs.items():
            if value is not None:
                updated[key] = value
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
    user_id, kwargs = svc.repo.last_args
    assert user_id == 1
    assert kwargs.get("name") == "New Name"
    # Other fields should be None
    assert kwargs.get("email") is None
    assert kwargs.get("picture") is None

def test_update_all_fields_maps_contact_dict(svc):
    req = ProfileUpdate(
        name="Neo",
        picture="p.png",
        contact_email="a@b.com",
        contact_phone="555",
    )
    out = svc.update(1, req)
    assert out.name == "Neo"
    user_id, kwargs = svc.repo.last_args
    assert user_id == 1
    assert kwargs.get("name") == "Neo"
    assert kwargs.get("picture") == "p.png"
    assert kwargs.get("contact_email") == "a@b.com"
    assert kwargs.get("contact_phone") == "555"
