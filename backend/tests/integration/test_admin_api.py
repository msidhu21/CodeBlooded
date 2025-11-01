import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.models.entities import Base
from app.core import db as core_db

@pytest.fixture(scope="function")
def client(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path/'t.db'}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def _get_db():
        d = TestingSessionLocal()
        try:
            yield d; d.commit()
        except:
            d.rollback(); raise
        finally:
            d.close()

    app = create_app()
    app.dependency_overrides[core_db.get_db] = _get_db
    return TestClient(app)

H = {"Authorization": "Bearer admin"}

def test_admin_crud_and_export(client: TestClient):
    p = {"sku":"M3A","name":"Alpha","category":"tools","available":True,"description":"d"}
    r = client.post("/admin/items", json=p, headers=H); assert r.status_code == 201
    iid = r.json()["id"]
    r2 = client.patch(f"/admin/items/{iid}", json={"name":"Alpha+"}, headers=H); assert r2.json()["name"] == "Alpha+"
    r3 = client.post("/export/selection", json={"ids":[iid]}, headers=H); assert r3.json()["count"] == 1
    r4 = client.delete(f"/admin/items/{iid}", headers=H); assert r4.status_code == 204

def test_duplicate_sku_409(client: TestClient):
    p = {"sku":"DUP","name":"X","category":"c","available":True,"description":""}
    assert client.post("/admin/items", json=p, headers=H).status_code == 201
    assert client.post("/admin/items", json=p, headers=H).status_code == 409

