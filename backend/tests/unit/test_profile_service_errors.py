import pytest

from app.services.profile_service import ProfileService
from app.models.dto import ProfileUpdate
from app.core.errors import NotFound


class BoomRepo:
    def update_profile(self, user_id, *, name=None, picture=None, contact=None):
        raise RuntimeError("boom")


class NotFoundRepo:
    def update_profile(self, user_id, *, name=None, picture=None, contact=None):
        raise NotFound("user not found")


def make_svc(repo):
    svc = ProfileService.__new__(ProfileService)
    svc.repo = repo
    return svc


def test_update_bubbles_runtime_error():
    svc = make_svc(BoomRepo())
    with pytest.raises(RuntimeError):
        svc.update(1, ProfileUpdate(name="X"))


def test_update_raises_not_found():
    svc = make_svc(NotFoundRepo())
    with pytest.raises(NotFound):
        svc.update(1, ProfileUpdate(name="X"))
