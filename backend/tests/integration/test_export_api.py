import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.models.entities import Base
from app.core import db as core_db


# Helper functions for authentication
def get_admin_headers(token: str = "admin") -> dict:
    """Get admin authorization headers.
    
    Args:
        token: Admin token (default: "admin")
        
    Returns:
        Dictionary with Authorization header
    """
    return {"Authorization": f"Bearer {token}"}


ADMIN_HEADERS = get_admin_headers()


# Helper functions for creating test data
def create_test_item(client: TestClient, sku: str, name: str, category: str = "tools", 
                     available: bool = True, description: str = "", 
                     headers: dict = None) -> int:
    """Create a test item via the admin API.
    
    Args:
        client: TestClient instance
        sku: Item SKU
        name: Item name
        category: Item category (default: "tools")
        available: Availability status (default: True)
        description: Item description (default: "")
        headers: Optional headers (defaults to ADMIN_HEADERS)
        
    Returns:
        Created item ID
    """
    if headers is None:
        headers = ADMIN_HEADERS
    payload = {
        "sku": sku,
        "name": name,
        "category": category,
        "available": available,
        "description": description
    }
    r = client.post("/admin/items", json=payload, headers=headers)
    assert r.status_code == 201, f"Failed to create item: {r.json()}"
    return r.json()["id"]


def create_multiple_items(client: TestClient, count: int, prefix: str = "EXP") -> list[int]:
    """Create multiple test items.
    
    Args:
        client: TestClient instance
        count: Number of items to create
        prefix: Prefix for SKU and name (default: "EXP")
        
    Returns:
        List of created item IDs
    """
    item_ids = []
    for i in range(count):
        item_id = create_test_item(client, f"{prefix}{i}", f"Item {i}")
        item_ids.append(item_id)
    return item_ids


# Helper functions for assertions
def assert_export_response_success(response, expected_count: int, expected_ids: list[int] = None) -> dict:
    """Assert that an export response is successful and matches expectations.
    
    Args:
        response: Response object from TestClient
        expected_count: Expected count of items
        expected_ids: Optional list of expected item IDs
        
    Returns:
        Parsed JSON response data
    """
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.json()}"
    assert "Content-Disposition" in response.headers
    assert "selection.json" in response.headers["Content-Disposition"]
    
    data = response.json()
    assert data["count"] == expected_count
    assert len(data["items"]) == expected_count
    
    if expected_ids:
        exported_ids = [item["id"] for item in data["items"]]
        assert set(exported_ids) == set(expected_ids)
    
    return data


def assert_export_response_error(response, expected_status: int, error_contains: str = None) -> dict:
    """Assert that an export response is an error.
    
    Args:
        response: Response object from TestClient
        expected_status: Expected HTTP status code
        error_contains: Optional string that should be in error detail
        
    Returns:
        Parsed JSON response data
    """
    assert response.status_code == expected_status
    data = response.json()
    if error_contains:
        assert error_contains in data.get("detail", "")
    return data


# Fixtures
@pytest.fixture(scope="function")
def client(tmp_path):
    """Fixture providing a TestClient with a fresh database for each test."""
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

# Test cases
def test_export_selection_requires_admin(client: TestClient):
    """Test that export endpoint requires admin authentication."""
    r = client.post("/export/selection", json={"ids": [1]})
    assert_export_response_error(r, expected_status=403)


def test_export_selection_empty_list(client: TestClient):
    """Test exporting with an empty ID list."""
    r = client.post("/export/selection", json={"ids": []}, headers=ADMIN_HEADERS)
    data = assert_export_response_success(r, expected_count=0)
    assert data["items"] == []


def test_export_selection_single_item(client: TestClient):
    """Test exporting a single item."""
    item_id = create_test_item(client, "EXP1", "Export Item 1", description="test")
    
    r = client.post("/export/selection", json={"ids": [item_id]}, headers=ADMIN_HEADERS)
    data = assert_export_response_success(r, expected_count=1, expected_ids=[item_id])
    
    item = data["items"][0]
    assert item["id"] == item_id
    assert item["sku"] == "EXP1"
    assert item["name"] == "Export Item 1"
    assert item["description"] == "test"


def test_export_selection_multiple_items(client: TestClient):
    """Test exporting multiple items."""
    item_ids = create_multiple_items(client, count=3)
    
    r = client.post("/export/selection", json={"ids": item_ids}, headers=ADMIN_HEADERS)
    assert_export_response_success(r, expected_count=3, expected_ids=item_ids)


def test_export_selection_invalid_ids(client: TestClient):
    """Test exporting with all invalid IDs."""
    r = client.post("/export/selection", json={"ids": [999, 1000]}, headers=ADMIN_HEADERS)
    assert_export_response_error(r, expected_status=400, error_contains="Items not found")


def test_export_selection_partial_invalid_ids(client: TestClient):
    """Test exporting with mix of valid and invalid IDs."""
    valid_id = create_test_item(client, "VALID", "Valid Item")
    
    r = client.post("/export/selection", json={"ids": [valid_id, 999]}, headers=ADMIN_HEADERS)
    data = assert_export_response_error(r, expected_status=400, error_contains="Items not found")
    assert "999" in data["detail"]
    assert str(valid_id) not in data["detail"]


def test_export_selection_response_format(client: TestClient):
    """Test that export response has correct format and all required fields."""
    item_id = create_test_item(client, "FORMAT", "Format Test", description="desc")
    
    r = client.post("/export/selection", json={"ids": [item_id]}, headers=ADMIN_HEADERS)
    data = assert_export_response_success(r, expected_count=1)
    
    # Verify response structure
    assert "count" in data
    assert "items" in data
    assert isinstance(data["count"], int)
    assert isinstance(data["items"], list)
    
    # Verify item structure
    item = data["items"][0]
    required_fields = ["id", "sku", "name", "category", "available", "description"]
    for field in required_fields:
        assert field in item, f"Missing field: {field}"


def test_export_selection_without_auth_header(client: TestClient):
    """Test that export fails without authorization header."""
    r = client.post("/export/selection", json={"ids": [1]})
    assert_export_response_error(r, expected_status=403)


def test_export_selection_with_invalid_token(client: TestClient):
    """Test that export fails with invalid token."""
    invalid_headers = get_admin_headers(token="invalid")
    r = client.post("/export/selection", json={"ids": [1]}, headers=invalid_headers)
    assert_export_response_error(r, expected_status=403)


def test_export_selection_missing_json_body(client: TestClient):
    """Test that export fails when JSON body is missing."""
    r = client.post("/export/selection", headers=ADMIN_HEADERS)
    # FastAPI typically returns 422 for missing/invalid request body
    assert r.status_code in [400, 422]


def test_export_selection_large_id_list(client: TestClient):
    """Test exporting with a large list of IDs (50 items)."""
    # Create 50 items
    item_ids = create_multiple_items(client, count=50, prefix="LARGE")
    
    # Export all 50 items
    r = client.post("/export/selection", json={"ids": item_ids}, headers=ADMIN_HEADERS)
    data = assert_export_response_success(r, expected_count=50, expected_ids=item_ids)
    
    # Verify all items are present
    exported_ids = [item["id"] for item in data["items"]]
    assert len(exported_ids) == 50
    assert set(exported_ids) == set(item_ids)

