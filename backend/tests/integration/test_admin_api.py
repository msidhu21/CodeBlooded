import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.models.entities import Base
from app.core import deps

@pytest.fixture(scope="function")
def client(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def _get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
            db.commit()
        except:
            db.rollback()
            raise
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[deps.get_db] = _get_test_db
    app.dependency_overrides[deps.require_admin] = lambda: {"role": "admin"}
    return TestClient(app)

ADMIN_HEADERS = {"Authorization": "Bearer admin"}

def test_admin_create_update_delete_item(client: TestClient):
    payload = {"sku":"A100","name":"Alpha","category":"tools","available":True,"description":"d"}
    r = client.post("/admin/items", json=payload, headers=ADMIN_HEADERS)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["id"] > 0 and item["sku"] == "A100"

    r2 = client.patch(f"/admin/items/{item['id']}", json={"name":"Alpha+"}, headers=ADMIN_HEADERS)
    assert r2.status_code == 200
    assert r2.json()["name"] == "Alpha+"

    r3 = client.delete(f"/admin/items/{item['id']}", headers=ADMIN_HEADERS)
    assert r3.status_code == 204

def test_duplicate_sku_conflict(client: TestClient):
    p = {"sku":"DUP","name":"X","category":"c","available":True,"description":""}
    r1 = client.post("/admin/items", json=p, headers=ADMIN_HEADERS)
    r2 = client.post("/admin/items", json=p, headers=ADMIN_HEADERS)
    assert r2.status_code == 409

