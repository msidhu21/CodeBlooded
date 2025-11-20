import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    app = create_app()
    return TestClient(app)


def test_search_api_response_structure(client):
    """Test that search API returns correct response structure"""
    response = client.get("/items/search?q=cable")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check main keys exist
    assert "products" in data
    assert "pagination" in data
    assert "filters_applied" in data
    assert "meta" in data
    
    # Check pagination structure
    pagination = data["pagination"]
    assert "page" in pagination
    assert "size" in pagination
    assert "total_results" in pagination
    assert "total_pages" in pagination
    assert "has_more" in pagination
    
    # Check filters structure
    filters = data["filters_applied"]
    assert "search_query" in filters
    assert "category" in filters
    assert "min_rating" in filters
    assert "max_price" in filters
    
    # Check meta structure
    meta = data["meta"]
    assert "search_time_ms" in meta
    assert "results_on_page" in meta


def test_search_api_with_multiple_filters(client):
    """Test search API with category and rating filters"""
    response = client.get("/items/search?q=usb&category=cables&min_rating=4.0")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify filters are recorded
    assert data["filters_applied"]["search_query"] == "usb"
    assert data["filters_applied"]["category"] == "cables"
    assert data["filters_applied"]["min_rating"] == 4.0
    
    # Verify products match filters (if any returned)
    if data["products"]:
        for product in data["products"]:
            # Rating might be string or None, convert to float for comparison
            rating = float(product["rating"]) if product["rating"] else 0
            assert rating >= 4.0


def test_search_api_pagination_metadata(client):
    """Test that pagination metadata is accurate"""
    response = client.get("/items/search?q=cable&page=1&size=5")
    
    assert response.status_code == 200
    data = response.json()
    
    pagination = data["pagination"]
    assert pagination["page"] == 1
    assert pagination["size"] == 5
    assert pagination["total_results"] >= 0
    
    # has_more should be True if there are more pages
    if pagination["total_results"] > 5:
        assert pagination["has_more"] == True
        assert pagination["total_pages"] > 1
    else:
        assert pagination["has_more"] == False


def test_search_api_empty_results(client):
    """Test search API with no matching results"""
    response = client.get("/items/search?q=NonExistentProductXYZ123")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["products"] == []
    assert data["pagination"]["total_results"] == 0
    assert data["pagination"]["total_pages"] == 0
    assert data["pagination"]["has_more"] == False
    assert data["meta"]["results_on_page"] == 0


def test_search_api_performance_timing(client):
    """Test that search timing is recorded"""
    response = client.get("/items/search?q=cable")
    
    assert response.status_code == 200
    data = response.json()
    
    # Search time should be a positive number
    assert data["meta"]["search_time_ms"] > 0
    assert isinstance(data["meta"]["search_time_ms"], (int, float))


def test_search_api_without_query(client):
    """Test search API without query parameter"""
    response = client.get("/items/search")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return results (all products with pagination)
    assert "products" in data
    assert data["filters_applied"]["search_query"] is None


def test_search_api_results_count_matches(client):
    """Test that results_on_page matches actual product count"""
    response = client.get("/items/search?q=cable&size=3")
    
    assert response.status_code == 200
    data = response.json()
    
    actual_count = len(data["products"])
    reported_count = data["meta"]["results_on_page"]
    
    assert actual_count == reported_count


def test_search_api_max_price_filter(client):
    """Test search with max price filter"""
    response = client.get("/items/search?max_price=500")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["filters_applied"]["max_price"] == 500
    
    # All returned products should be under max price (if any)
    for product in data["products"]:
        # Extract numeric price from string like "₹299"
        price_str = product["discounted_price"].replace("₹", "").replace(",", "")
        price = float(price_str)
        assert price <= 500
