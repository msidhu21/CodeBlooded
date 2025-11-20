"""Unit tests for multi-attribute filtering"""
import pytest
import pandas as pd
from app.repos.csv_repo import CSVRepository


@pytest.fixture
def filter_test_csv(tmp_path):
    """Create a test CSV with products at various price points and discounts"""
    test_data = pd.DataFrame({
        'product_id': ['F1', 'F2', 'F3', 'F4', 'F5'],
        'product_name': ['Budget Phone', 'Mid Phone', 'Premium Phone', 'Budget Laptop', 'Premium Laptop'],
        'category': ['Electronics|Phones', 'Electronics|Phones', 'Electronics|Phones', 
                    'Electronics|Laptops', 'Electronics|Laptops'],
        'discounted_price': ['₹5,000', '₹15,000', '₹50,000', '₹25,000', '₹80,000'],
        'actual_price': ['₹10,000', '₹20,000', '₹60,000', '₹35,000', '₹100,000'],
        'discount_percentage': ['50%', '25%', '17%', '29%', '20%'],
        'rating': [3.5, 4.0, 4.5, 3.8, 4.8],
        'rating_count': [100, 200, 500, 150, 300],
        'about_product': ['Budget option', 'Good value', 'Best quality', 'Work laptop', 'Gaming laptop'],
        'user_id': ['U1', 'U2', 'U3', 'U4', 'U5'],
        'user_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'review_id': ['R1', 'R2', 'R3', 'R4', 'R5'],
        'review_title': ['Good', 'Great', 'Excellent', 'Nice', 'Perfect'],
        'review_content': ['Good phone', 'Great phone', 'Best phone', 'Nice laptop', 'Perfect laptop'],
        'img_link': ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg'],
        'product_link': ['link1', 'link2', 'link3', 'link4', 'link5']
    })
    
    csv_path = tmp_path / "filter_products.csv"
    test_data.to_csv(csv_path, index=False)
    return str(csv_path)


def test_price_range_filter(filter_test_csv):
    """Test filtering by price range"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    # Products between 10,000 and 30,000
    results = repo.search_products(min_price=10000, max_price=30000)
    
    assert len(results) == 2  # Mid Phone and Budget Laptop
    assert all(10000 <= float(p['discounted_price'].replace('₹', '').replace(',', '')) <= 30000 
              for p in results)


def test_min_price_only(filter_test_csv):
    """Test filtering with only minimum price"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    results = repo.search_products(min_price=50000)
    
    assert len(results) == 2  # Premium Phone and Premium Laptop
    prices = [float(p['discounted_price'].replace('₹', '').replace(',', '')) for p in results]
    assert all(price >= 50000 for price in prices)


def test_max_price_only(filter_test_csv):
    """Test filtering with only maximum price"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    results = repo.search_products(max_price=20000)
    
    assert len(results) == 2  # Budget Phone and Mid Phone
    prices = [float(p['discounted_price'].replace('₹', '').replace(',', '')) for p in results]
    assert all(price <= 20000 for price in prices)


def test_discount_filter(filter_test_csv):
    """Test filtering by minimum discount percentage"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    # Products with at least 25% discount
    results = repo.search_products(min_discount=25)
    
    assert len(results) == 3  # Budget Phone (50%), Mid Phone (25%), Budget Laptop (29%)
    discounts = [float(p['discount_percentage'].replace('%', '')) for p in results]
    assert all(discount >= 25 for discount in discounts)


def test_rating_range_filter(filter_test_csv):
    """Test filtering by rating range"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    # Products rated between 4.0 and 4.5
    results = repo.search_products(min_rating=4.0, max_rating=4.5)
    
    assert len(results) == 2  # Mid Phone (4.0) and Premium Phone (4.5)
    ratings = [p['rating'] for p in results]
    assert all(4.0 <= rating <= 4.5 for rating in ratings)


def test_combined_filters(filter_test_csv):
    """Test combining multiple filters"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    # Phones under 20,000 with at least 4.0 rating
    results = repo.search_products(
        category='Phones',
        max_price=20000,
        min_rating=4.0
    )
    
    assert len(results) == 1  # Only Mid Phone matches all criteria
    product = results[0]
    assert 'Phones' in product['category']
    assert float(product['discounted_price'].replace('₹', '').replace(',', '')) <= 20000
    assert product['rating'] >= 4.0


def test_text_search_with_filters(filter_test_csv):
    """Test combining text search with filters"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    # Search for "laptop" with minimum rating and max price
    results = repo.search_products(
        query='laptop',
        min_rating=4.0,
        max_price=30000
    )
    
    assert len(results) == 0  # Budget Laptop doesn't meet rating requirement
    
    # Now with lower rating threshold
    results = repo.search_products(
        query='laptop',
        min_rating=3.5,
        max_price=30000
    )
    
    assert len(results) == 1  # Budget Laptop
    assert 'Laptop' in results[0]['product_name']


def test_all_filters_combined(filter_test_csv):
    """Test using all available filters together"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    results = repo.search_products(
        query='Phone',
        category='Electronics',
        min_rating=3.5,
        max_rating=4.5,
        min_price=5000,
        max_price=50000,
        min_discount=17
    )
    
    # Should return all 3 phones as they all match these broad criteria
    assert len(results) == 3


def test_return_total_count(filter_test_csv):
    """Test that return_total flag works correctly"""
    repo = CSVRepository(csv_path=filter_test_csv)
    
    results, total = repo.search_products(
        category='Phones',
        limit=2,
        return_total=True
    )
    
    assert len(results) == 2  # Limited to 2
    assert total == 3  # Total phones available
    
    # Test with pagination
    results_page2, total_page2 = repo.search_products(
        category='Phones',
        limit=2,
        offset=2,
        return_total=True
    )
    
    assert len(results_page2) == 1  # Only 1 item on page 2
    assert total_page2 == 3  # Total still 3
