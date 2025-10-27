import pytest
from types import SimpleNamespace
from app.services.export_service import ExportService
from app.models.dto import ExportSelectionRequest

class FakeRepo:
    def __init__(self, items):
        self._items = items
    def get_many(self, ids):
        return [i for i in self._items if i.id in ids]

def make_item(id, **kw):
    d = dict(sku=f"SKU{id}", name=f"Item{id}", category="cat", available=True, description="")
    d.update(kw)
    return SimpleNamespace(id=id, **d)

def test_export_selection_returns_only_requested_ids():
    items = [make_item(1), make_item(2), make_item(3)]
    svc = ExportService(FakeRepo(items))
    out = svc.export_selection(ExportSelectionRequest(ids=[1,3]))
    assert out.count == 2
    assert [x.id for x in out.items] == [1,3]

def test_export_selection_empty_ids_is_ok():
    svc = ExportService(FakeRepo([]))
    out = svc.export_selection(ExportSelectionRequest(ids=[]))
    assert out.count == 0
    assert out.items == []

