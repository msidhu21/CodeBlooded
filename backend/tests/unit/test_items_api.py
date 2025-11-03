import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_item_details_found(monkeypatch):
    class DummyItem:
        id = 1
        sku = "sku1"
        name = "Test Item"
        category = "cat1"
        available = True
        description = "desc"
    class DummyQuery:
        def filter(self, *args, **kwargs):
            return self
        def limit(self, n):
            return self
        def scalars(self):
            class DummyScalars:
                def all(self_inner):
                    return []
            return DummyScalars()
    class DummyDB:
        def query(self, model):
            return DummyQuery()
    class DummyRepo:
        def __init__(self, db):
            self.db = db
        def by_id(self, item_id):
            if item_id == 1:
                return DummyItem()
            return None
    # Patch ItemRepo to use DummyRepo and provide DummyDB
    monkeypatch.setattr("app.api.items.ItemRepo", DummyRepo)
    monkeypatch.setattr("app.api.items.get_db", lambda: DummyDB())
    monkeypatch.setattr("app.api.items.get_related_items", lambda item, db: [])
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["id"] == 1
    assert data["item"]["name"] == "Test Item"
    assert isinstance(data["related"], list)

def test_get_item_details_not_found(monkeypatch):
    class DummyRepo:
        def __init__(self, db): pass
        def by_id(self, item_id):
            return None
        db = None
    monkeypatch.setattr("app.api.items.ItemRepo", DummyRepo)
    monkeypatch.setattr("app.api.items.get_db", lambda: None)
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
