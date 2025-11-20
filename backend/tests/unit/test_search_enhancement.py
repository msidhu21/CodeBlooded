import pytest
from app.repos.csv_repo import CSVRepository
import pandas as pd


@pytest.fixture
def search_test_csv(tmp_path):
    """Create a CSV with varied data for testing search"""
    csv_file = tmp_path / "search_products.csv"
    test_data = pd.DataFrame([
        {
            'product_id': 'P001',
            'product_name': 'USB Cable for iPhone',
            'category': 'Cables',
            'discounted_price': '₹299',
            'actual_price': '₹599',
            'rating': 4.2,
            'about_product': 'Fast charging cable compatible with iPhone devices'
        },
        {
            'product_id': 'P002',
            'product_name': 'Wireless Mouse',
            'category': 'Accessories',
            'discounted_price': '₹499',
            'actual_price': '₹899',
            'rating': 4.5,
            'about_product': 'Ergonomic wireless mouse for desktop and laptop'
        },
        {
            'product_id': 'P003',
            'product_name': 'Laptop Charger',
            'category': 'Cables',
            'discounted_price': '₹799',
            'actual_price': '₹1299',
            'rating': 4.0,
            'about_product': 'Universal laptop charger with fast charging support'
        },
        {
            'product_id': 'P004',
            'product_name': 'Keyboard USB Wired',
            'category': 'Accessories',
            'discounted_price': '₹599',
            'actual_price': '₹999',
            'rating': 4.7,
            'about_product': 'Mechanical keyboard with USB connection for gaming'
        },
        {
            'product_id': 'P005',
            'product_name': 'Monitor Stand',
            'category': 'Furniture',
            'discounted_price': '₹1299',
            'actual_price': '₹1999',
            'rating': 3.8,
            'about_product': 'Adjustable monitor stand for better ergonomics'
        }
    ])
    test_data.to_csv(csv_file, index=False)
    return str(csv_file)


def test_search_by_product_name(search_test_csv):
    """Test searching by product name"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="USB")
    
    assert len(results) == 2  # USB Cable and Keyboard USB
    product_ids = [p['product_id'] for p in results]
    assert 'P001' in product_ids
    assert 'P004' in product_ids


def test_search_by_description(search_test_csv):
    """Test searching in product descriptions"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="fast charging")
    
    assert len(results) == 2  # USB Cable and Laptop Charger both mention fast charging
    product_ids = [p['product_id'] for p in results]
    assert 'P001' in product_ids
    assert 'P003' in product_ids


def test_search_by_category(search_test_csv):
    """Test searching by category"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="Cables")
    
    assert len(results) == 2  # USB Cable and Laptop Charger
    for result in results:
        assert result['category'] == 'Cables'


def test_search_relevance_ranking(search_test_csv):
    """Test that results are ranked by relevance"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="USB")
    
    # USB Cable should be first (USB in name)
    # Keyboard USB should be second (USB in name)
    assert results[0]['product_id'] == 'P001' or results[0]['product_id'] == 'P004'
    assert results[0]['product_name'].lower().find('usb') != -1


def test_search_case_insensitive(search_test_csv):
    """Test that search is case insensitive"""
    repo = CSVRepository(csv_path=search_test_csv)
    results_lower = repo.search_products(query="usb")
    results_upper = repo.search_products(query="USB")
    results_mixed = repo.search_products(query="Usb")
    
    assert len(results_lower) == len(results_upper) == len(results_mixed)


def test_search_with_category_filter(search_test_csv):
    """Test search combined with category filter"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="USB", category="Cables")
    
    assert len(results) == 1
    assert results[0]['product_id'] == 'P001'
    assert results[0]['category'] == 'Cables'


def test_search_with_rating_filter(search_test_csv):
    """Test search combined with minimum rating filter"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="USB", min_rating=4.5)
    
    assert len(results) == 1
    assert results[0]['product_id'] == 'P004'  # Keyboard has 4.7 rating
    assert results[0]['rating'] >= 4.5


def test_search_with_price_filter(search_test_csv):
    """Test search combined with max price filter"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="USB", max_price=500)
    
    # Only USB Cable at 299 should match
    assert len(results) == 1
    assert results[0]['product_id'] == 'P001'


def test_search_with_all_filters(search_test_csv):
    """Test search with all filters combined"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(
        query="charging",
        category="Cables",
        min_rating=4.0,
        max_price=1000
    )
    
    assert len(results) == 2  # USB Cable and Laptop Charger
    for result in results:
        assert result['category'] == 'Cables'
        assert result['rating'] >= 4.0


def test_search_with_pagination(search_test_csv):
    """Test search with pagination"""
    repo = CSVRepository(csv_path=search_test_csv)
    
    # Get first page
    page1 = repo.search_products(query="a", limit=2, offset=0)
    assert len(page1) == 2
    
    # Get second page
    page2 = repo.search_products(query="a", limit=2, offset=2)
    assert len(page2) <= 2
    
    # Verify different results
    page1_ids = [p['product_id'] for p in page1]
    page2_ids = [p['product_id'] for p in page2]
    assert page1_ids != page2_ids


def test_search_return_total_count(search_test_csv):
    """Test that return_total parameter works"""
    repo = CSVRepository(csv_path=search_test_csv)
    results, total = repo.search_products(query="a", limit=2, offset=0, return_total=True)
    
    assert isinstance(results, list)
    assert isinstance(total, int)
    assert total >= len(results)
    assert len(results) <= 2  # Respects limit


def test_search_no_results(search_test_csv):
    """Test search with no matching results"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query="NonExistentProduct123")
    
    assert len(results) == 0
    assert results == []


def test_search_empty_query(search_test_csv):
    """Test search with no query returns all products"""
    repo = CSVRepository(csv_path=search_test_csv)
    results = repo.search_products(query=None)
    
    assert len(results) == 5  # All products
