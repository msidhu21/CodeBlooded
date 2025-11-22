import pandas as pd
from pathlib import Path
from app.repos.user_repo import UserRepo
from app.core.errors import Conflict, NotFound


# I made this helper to quickly create a fake users.csv for each test
def make_sample_csv(path: Path):
    df = pd.DataFrame(
        [
            {
                "user_id": 1,
                "email": "admin@cosc310.ca",
                "password_hash": "hash1",
                "name": "Admin",
                "role": "admin",
            },
            {
                "user_id": 2,
                "email": "user@cosc310.ca",
                "password_hash": "hash2",
                "name": "Normal User",
                "role": "user",
            },
        ]
    )
    df.to_csv(path, index=False)


def test_by_email_found(tmp_path):
    # here I'm setting up a temp CSV file just for this test
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    user = repo.by_email("admin@cosc310.ca")

    # I expect to actually find this user
    assert user is not None
    assert user["email"] == "admin@cosc310.ca"
    assert int(user["user_id"]) == 1


def test_by_email_not_found(tmp_path):
    # same idea as above, but using an email that does not exist
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    user = repo.by_email("doesnotexist@example.com")

    # this should be None when the user is not there
    assert user is None


def test_by_id_found(tmp_path):
    # checking that by_id works when the id exists
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    user = repo.by_id(2)

    # I know user_id 2 is Normal User from the sample CSV
    assert user["email"] == "user@cosc310.ca"
    assert user["name"] == "Normal User"


def test_by_id_not_found_raises(tmp_path):
    # here I want to make sure NotFound is raised for a bad id
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    try:
        repo.by_id(999)
        # if it does not raise, then the test should fail
        assert False, "Expected NotFound but nothing was raised"
    except NotFound:
        # this is what I want to happen
        assert True


def test_create_adds_user_and_increments_id(tmp_path):
    # testing that create() gives a new id and saves properly
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    new = repo.create(
        email="newuser@cosc310.ca",
        password_hash="hash3",
        name="New User",
        role="user",
    )

    # I already had ids 1 and 2, so this should be 3
    assert int(new["user_id"]) == 3
    assert new["email"] == "newuser@cosc310.ca"

    # double-check by reading it back through the repo
    again = repo.by_email("newuser@cosc310.ca")
    assert again is not None
    assert int(again["user_id"]) == 3


def test_create_conflict_on_duplicate_email(tmp_path):
    # here I want to confirm that duplicate emails are blocked
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    # first create for this email should be fine
    repo.create(
        email="extra@cosc310.ca",
        password_hash="hash4",
        name="Extra User",
        role="user",
    )

    # second create with the same email should trigger Conflict
    try:
        repo.create(
            email="extra@cosc310.ca",
            password_hash="hash5",
            name="Another User",
            role="user",
        )
        assert False, "Expected Conflict but nothing was raised"
    except Conflict:
        assert True


def test_update_profile_changes_name(tmp_path):
    # testing that update_profile actually changes the name and saves it
    csv_path = tmp_path / "users.csv"
    make_sample_csv(csv_path)

    repo = UserRepo(csv_path=str(csv_path))

    updated = repo.update_profile(user_id=2, name="Updated Name")

    assert updated["name"] == "Updated Name"

    again = repo.by_id(2)
    assert again["name"] == "Updated Name"
