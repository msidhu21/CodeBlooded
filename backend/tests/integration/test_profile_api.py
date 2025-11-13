from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
import shutil, os

REAL_CSV = Path(__file__).parents[2] / "data" / "users.csv"  # backend/data/users.csv
SAFE_CSV = Path("C:/Temp/users_test.csv")  # outside OneDrive

def test_patch_profile_against_real_copy(monkeypatch):
    SAFE_CSV.parent.mkdir(parents=True, exist_ok=True)
    # copy real -> safe location
    shutil.copyfile(REAL_CSV, SAFE_CSV)

    # point repo at safe copy (NOT the OneDrive file)
    monkeypatch.setenv("USERS_CSV", str(SAFE_CSV))

    from app.api import profile
    app = FastAPI(title="profile-only")
    app.include_router(profile.router)

    try:
        with TestClient(app, raise_server_exceptions=True) as client:
            payload = {
                "name": "Admin Updated",
                "picture": "avatar_profile_test.png",
                "contact": {"email": "admin@cosc310.ca", "phone": "555-1234"},
            }
            r = client.patch("/profile", json=payload, timeout=6.0)
            assert r.status_code == 200, r.text
            body = r.json()
            assert body["id"] == 1
            assert body["name"] == "Admin Updated"

        # verify the safe copy changed
        txt = SAFE_CSV.read_text(encoding="utf-8")
        assert "avatar_profile_test.png" in txt
        assert "555-1234" in txt

    finally:
        # optional cleanup
        monkeypatch.delenv("USERS_CSV", raising=False)
        try:
            os.remove(SAFE_CSV)
        except FileNotFoundError:
            pass
