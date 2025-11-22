from types import SimpleNamespace
from app.services.export_service import ExportService
from app.models.dto import ExportSelectionRequest

def make_item(i):
    return SimpleNamespace(id=i, sku=f"S{i}", name=f"N{i}", category="c", available=True, description="")

def test_export_selection_basic():
    svc = ExportService(db=None)
    svc.repo = type("FakeRepo", (), {"get_products_by_ids": lambda self, ids: [make_item(1), make_item(3)]})()
    out = svc.export_selection(ExportSelectionRequest(ids=[1,3]))
    assert out.count == 2
    assert [x.id for x in out.items] == [1,3]

def test_export_selection_empty_repo_response():
    svc = ExportService(db=None)
    svc.repo = type("FakeRepo", (), {"get_products_by_ids": lambda self, ids: []})()
    out = svc.export_selection(ExportSelectionRequest(ids=[1]))
    assert out.count == 0
