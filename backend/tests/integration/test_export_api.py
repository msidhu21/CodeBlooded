import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.models.entities import Base
from app.core import db as core_db

ADMIN_HEADERS = {"Authorization": "Bearer admin"}

@pytest.fixture(scope="function")
def client(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path/'t.db'}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def _get_db():
        d = TestingSessionLocal()
        try:
            yield d
            d.commit()
        except:
            d.rollback()
            raise
        finally:
            d.close()

    app = create_app()
    app.dependency_overrides[core_db.get_db] = _get_db
    return TestClient(app)

def create_test_item(client, sku, name, category="tools", available=True, description=""):
    payload = {"sku": sku, "name": name, "category": category, "available": available, "description": description}
    r = client.post("/admin/items", json=payload, headers=ADMIN_HEADERS)
    assert r.status_code == 201
    return r.json()["id"]

def test_export_selection_requires_admin(client: TestClient):
    r = client.post("/export/selection", json={"ids": [1]})
    assert r.status_code == 403

def test_export_selection_empty_list(client: TestClient):
    r = client.post("/export/selection", json={"ids": []}, headers=ADMIN_HEADERS)
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 0
    assert data["items"] == []
    assert "Content-Disposition" in r.headers
    assert "selection.json" in r.headers["Content-Disposition"]

def test_export_selection_single_item(client: TestClient):
    item_id = create_test_item(client, "EXP1", "Export Item 1", description="test")

    r = client.post("/export/selection", json={"ids": [item_id]}, headers=ADMIN_HEADERS)
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == item_id
    assert data["items"][0]["sku"] == "EXP1"
    assert data["items"][0]["name"] == "Export Item 1"

def test_export_selection_multiple_items(client: TestClient):
    item_ids = []
    for i in range(3):
        item_id = create_test_item(client, f"EXP{i}", f"Item {i}")
        item_ids.append(item_id)

    r = client.post("/export/selection", json={"ids": item_ids}, headers=ADMIN_HEADERS)
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 3
    assert len(data["items"]) == 3
    exported_ids = [item["id"] for item in data["items"]]
    assert set(exported_ids) == set(item_ids)

def test_export_selection_invalid_ids(client: TestClient):
    r = client.post("/export/selection", json={"ids": [999, 1000]}, headers=ADMIN_HEADERS)
    assert r.status_code == 400
    assert "Items not found" in r.json()["detail"]

def test_export_selection_partial_invalid_ids(client: TestClient):
    valid_id = create_test_item(client, "VALID", "Valid Item")

    r = client.post("/export/selection", json={"ids": [valid_id, 999]}, headers=ADMIN_HEADERS)
    assert r.status_code == 400
    assert "Items not found" in r.json()["detail"]
    assert "999" in r.json()["detail"]

def test_export_selection_response_format(client: TestClient):
    item_id = create_test_item(client, "FORMAT", "Format Test", description="desc")

    r = client.post("/export/selection", json={"ids": [item_id]}, headers=ADMIN_HEADERS)
    assert r.status_code == 200
    data = r.json()
    assert "count" in data
    assert "items" in data
    assert isinstance(data["count"], int)
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
    item = data["items"][0]
    assert "id" in item
    assert "sku" in item
    assert "name" in item
    assert "category" in item
    assert "available" in item
    assert "description" in item

def test_export_selection_without_auth_header(client: TestClient):
    r = client.post("/export/selection", json={"ids": [1]})
    assert r.status_code == 403

def test_export_selection_with_invalid_token(client: TestClient):
    r = client.post("/export/selection", json={"ids": [1]}, headers={"Authorization": "Bearer invalid"})
    assert r.status_code == 403

