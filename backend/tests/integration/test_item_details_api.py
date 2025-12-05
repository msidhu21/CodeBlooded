import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
from pathlib import Path

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    """Setup test data in the CSV before running tests"""
    # This assumes the real amazon.csv exists
    # In a real test environment, you might want to use a separate test CSV
    pass

def test_get_item_details_success():
    """Test GET /items/{product_id} returns product details and related items"""
    # Using a known product_id from the amazon.csv
    response = client.get("/items/B07JW9H4J1")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify product details are returned
    assert "product" in data
    assert "related" in data
    
    product = data["product"]
    assert product["product_id"] == "B07JW9H4J1"
    assert "product_name" in product
    assert "category" in product
    assert "discounted_price" in product
    assert "actual_price" in product
    assert "rating" in product
    assert "about_product" in product
    
    # Verify related items are returned
    related = data["related"]
    assert isinstance(related, list)
    assert len(related) <= 4  # Should return max 4 related items
    
    # Verify related items are in same category
    if len(related) > 0:
        product_category = product["category"]
        for item in related:
            assert item["category"] == product_category
            # Verify current product is not in related items
            assert item["product_id"] != product["product_id"]

def test_get_item_details_not_found():
    """Test GET /items/{product_id} returns 404 for non-existent product"""
    response = client.get("/items/NONEXISTENT_ID_12345")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_get_item_details_response_structure():
    """Test that item details response has correct structure"""
    response = client.get("/items/B07JW9H4J1")
    
    assert response.status_code == 200
    data = response.json()
    
    # Test top-level structure
    assert set(data.keys()) == {"product", "related"}
    
    # Test product structure contains expected fields
    product = data["product"]
    expected_fields = [
        "product_id", "product_name", "category", 
        "discounted_price", "actual_price", "rating"
    ]
    for field in expected_fields:
        assert field in product, f"Missing field: {field}"

def test_get_item_details_performance():
    """Test that item details endpoint responds quickly"""
    import time
    
    start = time.time()
    response = client.get("/items/B07JW9H4J1")
    duration = time.time() - start
    
    assert response.status_code == 200
    # Should respond in less than 1 second (feasible load time)
    assert duration < 1.0, f"Response took {duration}s, expected < 1s"

def test_get_item_details_multiple_products():
    """Test retrieving details for multiple different products"""
    # Test with first few product IDs from CSV
    test_ids = ["B07JW9H4J1", "B098NS6PVG", "B096MSW6CT"]
    
    for product_id in test_ids:
        response = client.get(f"/items/{product_id}")
        
        if response.status_code == 200:
            data = response.json()
            assert data["product"]["product_id"] == product_id
            assert "related" in data

def test_related_items_same_category():
    """Test that all related items are from the same category"""
    response = client.get("/items/B07JW9H4J1")
    
    assert response.status_code == 200
    data = response.json()
    
    product_category = data["product"]["category"]
    related = data["related"]
    
    for item in related:
        assert item["category"] == product_category, \
            f"Related item {item['product_id']} has different category"

def test_related_items_excludes_current_product():
    """Test that related items don't include the current product"""
    product_id = "B07JW9H4J1"
    response = client.get(f"/items/{product_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    related_ids = [item["product_id"] for item in data["related"]]
    assert product_id not in related_ids, \
        "Current product should not be in related items"
