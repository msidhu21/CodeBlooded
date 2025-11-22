import pandas as pd
import threading

from app.repos.user_repo import UserRepo


def make_repo():
    repo = UserRepo.__new__(UserRepo)
    repo._lock = threading.RLock()  # Add the lock that __init__ would create
    repo.df = pd.DataFrame(
        [
            {
                "user_id": 1,
                "email": "admin@cosc310.ca",
                "password_hash": "hash",
                "name": "Admin User",
                "role": "admin",
                "phone": "",
                "avatar_url": "",
            }
        ]
    )
    repo._save = lambda: None
    return repo


def test_update_profile_updates_name_only():
    repo = make_repo()
    updated = repo.update_profile(1, name="New Name")

    assert updated["user_id"] == 1
    assert updated["name"] == "New Name"
    assert updated["email"] == "admin@cosc310.ca"
    assert updated["phone"] == ""


def test_update_profile_updates_phone_only():
    repo = make_repo()
    updated = repo.update_profile(1, phone="555-1234")

    assert updated["user_id"] == 1
    assert updated["phone"] == "555-1234"
    assert updated["name"] == "Admin User"
