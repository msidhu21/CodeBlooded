import pytest
from app.repos.csv_repo import CSVRepository
import pandas as pd
from pathlib import Path

@pytest.fixture
def temp_csv(tmp_path):
    """Create a temporary CSV file for testing"""
    csv_file = tmp_path / "test_products.csv"
    test_data = pd.DataFrame([
        {
            'product_id': 'TEST001',
            'product_name': 'Test Product 1',
            'category': 'Electronics',
            'discounted_price': '₹500',
            'actual_price': '₹1000',
            'discount_percentage': '50%',
            'rating': 4.5,
            'rating_count': '100',
            'about_product': 'This is a test product',
            'user_id': 'USER1',
            'user_name': 'Test User',
            'review_id': 'REV1',
            'review_title': 'Good',
            'review_content': 'Nice product',
            'img_link': 'http://example.com/img.jpg',
            'product_link': 'http://example.com/product'
        },
        {
            'product_id': 'TEST002',
            'product_name': 'Test Product 2',
            'category': 'Electronics',
            'discounted_price': '₹600',
            'actual_price': '₹1200',
            'discount_percentage': '50%',
            'rating': 4.0,
            'rating_count': '50',
            'about_product': 'Another test product',
            'user_id': 'USER2',
            'user_name': 'Test User 2',
            'review_id': 'REV2',
            'review_title': 'Great',
            'review_content': 'Excellent',
            'img_link': 'http://example.com/img2.jpg',
            'product_link': 'http://example.com/product2'
        },
        {
            'product_id': 'TEST003',
            'product_name': 'Test Product 3',
            'category': 'Books',
            'discounted_price': '₹300',
            'actual_price': '₹500',
            'discount_percentage': '40%',
            'rating': 4.8,
            'rating_count': '200',
            'about_product': 'A great book',
            'user_id': 'USER3',
            'user_name': 'Test User 3',
            'review_id': 'REV3',
            'review_title': 'Must read',
            'review_content': 'Amazing book',
            'img_link': 'http://example.com/img3.jpg',
            'product_link': 'http://example.com/product3'
        }
    ])
    test_data.to_csv(csv_file, index=False)
    return str(csv_file)

def test_get_product_by_id_success(temp_csv):
    """Test retrieving a product by ID returns full details"""
    repo = CSVRepository(csv_path=temp_csv)
    product = repo.get_product_by_id('TEST001')
    
    assert product is not None
    assert product['product_id'] == 'TEST001'
    assert product['product_name'] == 'Test Product 1'
    assert product['category'] == 'Electronics'
    assert product['rating'] == 4.5
    assert product['about_product'] == 'This is a test product'
    assert 'discounted_price' in product
    assert 'actual_price' in product

def test_get_product_by_id_not_found(temp_csv):
    """Test retrieving a non-existent product returns None"""
    repo = CSVRepository(csv_path=temp_csv)
    product = repo.get_product_by_id('NONEXISTENT')
    
    assert product is None

def test_get_related_products(temp_csv):
    """Test retrieving related products in same category"""
    repo = CSVRepository(csv_path=temp_csv)
    related = repo.get_related_products('TEST001', limit=4)
    
    assert len(related) == 1  # Only TEST002 is in same category
    assert related[0]['product_id'] == 'TEST002'
    assert related[0]['category'] == 'Electronics'

def test_get_related_products_excludes_current(temp_csv):
    """Test that related products don't include the current product"""
    repo = CSVRepository(csv_path=temp_csv)
    related = repo.get_related_products('TEST001', limit=4)
    
    # Verify current product is not in related items
    related_ids = [p['product_id'] for p in related]
    assert 'TEST001' not in related_ids

def test_get_related_products_empty_category(temp_csv):
    """Test related products when no other products in category"""
    repo = CSVRepository(csv_path=temp_csv)
    related = repo.get_related_products('TEST003', limit=4)
    
    assert len(related) == 0  # No other books in test data

def test_get_related_products_nonexistent_product(temp_csv):
    """Test related products for non-existent product"""
    repo = CSVRepository(csv_path=temp_csv)
    related = repo.get_related_products('NONEXISTENT', limit=4)
    
    assert related == []

def test_get_related_products_limit(temp_csv):
    """Test that related products respects the limit parameter"""
    repo = CSVRepository(csv_path=temp_csv)
    related = repo.get_related_products('TEST001', limit=1)
    
    assert len(related) <= 1
