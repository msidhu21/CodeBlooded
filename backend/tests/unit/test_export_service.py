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

def test_export_selection_large_list():
    svc = ExportService(db=None)
    ids = list(range(1, 101))
    items = [make_item(i) for i in ids]
    svc.repo = type("FakeRepo", (), {"get_products_by_ids": lambda self, ids: items})()
    out = svc.export_selection(ExportSelectionRequest(ids=ids))
    assert out.count == 100
