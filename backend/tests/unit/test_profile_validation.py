import pytest
from pydantic import ValidationError

from app.models.dto import ContactInfo, ProfileUpdate


def test_contact_info_valid_phone_ok():
    c = ContactInfo(email="a@b.com", phone="1234567")
    assert c.phone == "1234567"


@pytest.mark.parametrize("phone", ["123", "1" * 20])
def test_contact_info_invalid_phone_raises(phone):
    with pytest.raises(ValidationError):
        ContactInfo(email="a@b.com", phone=phone)


def test_profile_update_allows_missing_phone():
    req = ProfileUpdate(name="Test", contact=ContactInfo(email="a@b.com"))
    assert req.contact.phone is None
