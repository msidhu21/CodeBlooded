from app.models.entities import User


def test_user_has_profile_fields():
    # Check the columns on the SQLAlchemy model, no DB needed
    cols = set(User.__table__.columns.keys())

    # Core auth fields
    assert "email" in cols
    assert "password_hash" in cols

    # Profile-related fields we care about for this user story
    assert "name" in cols
    assert "role" in cols
