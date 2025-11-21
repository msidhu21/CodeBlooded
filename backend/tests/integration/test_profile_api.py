from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import profile
import app.services.profile_service as ps
from app.models.dto import ProfileUpdate, AuthUser


def test_patch_profile_smoke(monkeypatch):
    """
    Integration-ish test:
    - Build a FastAPI app
    - Mount ONLY the /profile router
    - Monkeypatch ProfileService.update so we don't touch CSV/OneDrive
    - Call PATCH /profile and assert the JSON shape
    """

    app = FastAPI(title="profile-only")
    app.include_router(profile.router)

    def fake_update(self, user_id: int, req: ProfileUpdate) -> AuthUser:
        return AuthUser(
            user_id=1,
            email="admin@cosc310.ca",
            name=req.name or "Admin User",
            role="admin",
        )

    monkeypatch.setattr(ps.ProfileService, "update", fake_update, raising=True)

    with TestClient(app, raise_server_exceptions=True) as client:
        resp = client.patch(
            "/profile",
            json={
                "name": "Patched",
                "picture": "x.png",
                "contact": {"email": "admin@cosc310.ca", "phone": "9999999"},
            },
            timeout=5.0,
        )

    assert resp.status_code == 200, resp.text
    body = resp.json()

    # If AuthUser uses alias user_id -> id, JSON key will still be "id"
    assert body["id"] == 1
    assert body["name"] == "Patched"
    assert body["email"] == "admin@cosc310.ca"
    assert body["role"] == "admin"
