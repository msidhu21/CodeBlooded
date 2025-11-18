from types import SimpleNamespace
import pytest
from app.services.export_service import ExportService
from app.models.dto import ExportSelectionRequest
from app.core.errors import BadRequest

def make_item(i):
    return SimpleNamespace(id=i, sku=f"S{i}", name=f"N{i}", category="c", available=True, description="")

@pytest.fixture
def export_service():
    svc = ExportService(db=None)
    return svc

def make_fake_repo(items_func):
    return type("FakeRepo", (), {"by_ids": lambda self, ids: items_func(ids)})()

def assert_bad_request_with_ids(exc_info, expected_ids):
    detail = str(exc_info.value.detail)
    assert "Items not found" in detail
    for expected_id in expected_ids:
        assert str(expected_id) in detail

def test_export_selection_basic(export_service):
    export_service.repo = make_fake_repo(lambda ids: [make_item(1), make_item(3)])
    out = export_service.export_selection(ExportSelectionRequest(ids=[1,3]))
    assert out.count == 2
    assert [x.id for x in out.items] == [1,3]

def test_export_selection_empty_list(export_service):
    export_service.repo = make_fake_repo(lambda ids: [])
    out = export_service.export_selection(ExportSelectionRequest(ids=[]))
    assert out.count == 0
    assert out.items == []

def test_export_selection_single_item(export_service):
    export_service.repo = make_fake_repo(lambda ids: [make_item(5)])
    out = export_service.export_selection(ExportSelectionRequest(ids=[5]))
    assert out.count == 1
    assert out.items[0].id == 5
    assert out.items[0].sku == "S5"

def test_export_selection_raises_for_missing_ids(export_service):
    export_service.repo = make_fake_repo(lambda ids: [])
    with pytest.raises(BadRequest) as exc_info:
        export_service.export_selection(ExportSelectionRequest(ids=[999, 1000]))
    assert_bad_request_with_ids(exc_info, [999, 1000])

def test_export_selection_raises_for_partial_missing(export_service):
    export_service.repo = make_fake_repo(lambda ids: [make_item(1)])
    with pytest.raises(BadRequest) as exc_info:
        export_service.export_selection(ExportSelectionRequest(ids=[1, 999, 1000]))
    assert_bad_request_with_ids(exc_info, [999, 1000])

def test_export_selection_returns_correct_count(export_service):
    export_service.repo = make_fake_repo(lambda ids: [make_item(i) for i in ids])
    out = export_service.export_selection(ExportSelectionRequest(ids=[1, 2, 3, 4, 5]))
    assert out.count == 5
    assert len(out.items) == 5

