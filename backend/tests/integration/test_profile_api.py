from pathlib import Path
from fastapi.testclient import TestClient
import pytest
from app.main import app

def test_patch_profile_happy_path(tmp_path, monkeypatch):
    # TEMP CSV (no OneDrive)
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / "users.csv"
    csv_path.write_text(
        "user_id,email,password_hash,name,role\n"
        "1,admin@cosc310.ca,hash,Admin User,admin\n",
        encoding="utf-8"
    )

    # point repo at the temp CSV
    monkeypatch.setenv("USERS_CSV", str(csv_path))

    # use context manager so the app shuts down cleanly
    with TestClient(app) as client:
        payload = {
            "name": "Admin Updated",
            "picture": "avatar.png",
            "contact": {"email": "admin@cosc310.ca", "phone": "555-1234"},
        }
        r = client.patch("/profile", json=payload)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["id"] == 1
        assert body["name"] == "Admin Updated"

    # verify file really changed
    txt = csv_path.read_text(encoding="utf-8")
    assert "avatar.png" in txt
    assert "555-1234" in txt

    # clean env
    monkeypatch.delenv("USERS_CSV", raising=False)
