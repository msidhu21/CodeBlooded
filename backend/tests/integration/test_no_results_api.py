"""Integration tests for no-results API behavior"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_with_no_results_includes_suggestions():
    """Test that API returns suggestions when no results found"""
    response = client.get("/items/search?q=xyznonexistent123")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have empty products
    assert len(data["products"]) == 0
    assert data["pagination"]["total_results"] == 0
    
    # Should include suggestions
    assert "suggestions" in data
    assert "original_query" in data["suggestions"]
    assert "popular_products" in data["suggestions"]
    assert "similar_categories" in data["suggestions"]
    assert "did_you_mean" in data["suggestions"]


def test_search_with_results_no_suggestions():
    """Test that API does not include suggestions when results found"""
    response = client.get("/items/search?q=cable")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have products
    assert len(data["products"]) > 0
    
    # Should NOT include suggestions
    assert "suggestions" not in data


def test_no_results_suggestions_structure():
    """Test the structure of suggestions response"""
    response = client.get("/items/search?q=nonexistentproduct")
    
    assert response.status_code == 200
    data = response.json()
    
    suggestions = data.get("suggestions", {})
    
    # Verify structure
    assert isinstance(suggestions["popular_products"], list)
    assert isinstance(suggestions["similar_categories"], list)
    assert isinstance(suggestions["did_you_mean"], list)
    assert suggestions["original_query"] == "nonexistentproduct"


def test_no_results_popular_products_formatted():
    """Test that popular products in suggestions are properly formatted"""
    response = client.get("/items/search?q=xyz999")
    
    assert response.status_code == 200
    data = response.json()
    
    suggestions = data.get("suggestions", {})
    popular = suggestions.get("popular_products", [])
    
    # Should have at least some popular products
    assert len(popular) > 0
    
    # Check formatting
    for product in popular:
        assert "product_id" in product
        assert "product_name" in product
        assert "discounted_price" in product
        assert "rating" in product


def test_no_results_without_query():
    """Test behavior when filters return no results but no query provided"""
    response = client.get("/items/search?min_price=999999999")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have no products
    assert len(data["products"]) == 0
    
    # Should NOT include suggestions (no query provided)
    assert "suggestions" not in data


def test_suggestions_with_similar_category():
    """Test that similar categories are suggested"""
    # Search for something that partially matches categories
    response = client.get("/items/search?q=electron")
    
    assert response.status_code == 200
    data = response.json()
    
    # May or may not have direct results, but if no results:
    if data["pagination"]["total_results"] == 0:
        suggestions = data.get("suggestions", {})
        # Should suggest similar categories
        assert "similar_categories" in suggestions
