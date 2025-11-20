"""Unit tests for no-results handling"""
import pytest
import pandas as pd
from app.repos.csv_repo import CSVRepository


@pytest.fixture
def no_results_test_csv(tmp_path):
    """Create a test CSV with various products"""
    test_data = pd.DataFrame({
        'product_id': ['N1', 'N2', 'N3', 'N4', 'N5'],
        'product_name': ['USB Cable Type-C', 'HDMI Cable 4K', 'Power Bank 10000mAh', 
                        'Wireless Mouse', 'Bluetooth Headphones'],
        'category': ['Electronics|Cables', 'Electronics|Cables', 'Electronics|PowerBanks',
                    'Electronics|Accessories', 'Electronics|Audio'],
        'discounted_price': ['₹299', '₹599', '₹899', '₹499', '₹1,299'],
        'actual_price': ['₹599', '₹999', '₹1,499', '₹799', '₹2,499'],
        'discount_percentage': ['50%', '40%', '40%', '38%', '48%'],
        'rating': [4.2, 4.5, 4.3, 4.0, 4.7],
        'rating_count': ['10000', '5000', '8000', '3000', '15000'],
        'about_product': ['Fast charging cable', 'High quality HDMI', 'Portable power', 
                         'Wireless connectivity', 'Active noise cancellation'],
        'user_id': ['U1', 'U2', 'U3', 'U4', 'U5'],
        'user_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'review_id': ['R1', 'R2', 'R3', 'R4', 'R5'],
        'review_title': ['Good', 'Great', 'Nice', 'Okay', 'Excellent'],
        'review_content': ['Good product', 'Great product', 'Nice product', 'Okay product', 'Excellent product'],
        'img_link': ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg'],
        'product_link': ['link1', 'link2', 'link3', 'link4', 'link5']
    })
    
    csv_path = tmp_path / "no_results_products.csv"
    test_data.to_csv(csv_path, index=False)
    return str(csv_path)


def test_get_popular_products(no_results_test_csv):
    """Test getting popular products based on rating count"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    popular = repo.get_popular_products(limit=3)
    
    assert len(popular) == 3
    # Should be sorted by rating count (Bluetooth Headphones has 15000)
    assert popular[0]['product_name'] == 'Bluetooth Headphones'


def test_get_similar_categories(no_results_test_csv):
    """Test finding similar categories"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    # Search for "cables"
    similar = repo.get_similar_categories('cables', limit=5)
    
    assert len(similar) >= 1
    assert any('Cables' in cat for cat in similar)


def test_get_similar_categories_no_match(no_results_test_csv):
    """Test similar categories when no match found"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    similar = repo.get_similar_categories('xyz123nonexistent', limit=5)
    
    assert len(similar) == 0


def test_suggest_alternatives_structure(no_results_test_csv):
    """Test that suggest_alternatives returns correct structure"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    suggestions = repo.suggest_alternatives('nonexistent')
    
    # Check structure
    assert 'original_query' in suggestions
    assert 'similar_categories' in suggestions
    assert 'popular_products' in suggestions
    assert 'did_you_mean' in suggestions
    
    assert suggestions['original_query'] == 'nonexistent'


def test_suggest_alternatives_with_match(no_results_test_csv):
    """Test suggestions when category matches exist"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    suggestions = repo.suggest_alternatives('cable')
    
    # Should suggest similar categories
    assert len(suggestions['similar_categories']) > 0
    assert any('Cables' in cat for cat in suggestions['similar_categories'])
    
    # Should have popular products
    assert len(suggestions['popular_products']) > 0


def test_suggest_alternatives_popular_products(no_results_test_csv):
    """Test that popular products are included in suggestions"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    suggestions = repo.suggest_alternatives('xyz')
    
    # Even with no match, should return popular products
    assert len(suggestions['popular_products']) > 0
    assert len(suggestions['popular_products']) <= 5


def test_popular_products_compact_format(no_results_test_csv):
    """Test that popular products in suggestions are in compact format"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    suggestions = repo.suggest_alternatives('xyz')
    
    # Popular products should be formatted
    for product in suggestions['popular_products']:
        assert 'product_id' in product
        assert 'product_name' in product
        assert 'discounted_price' in product
        # Compact format should not include full description
        assert 'about_product' not in product


def test_similar_strings_method(no_results_test_csv):
    """Test the string similarity helper method"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    # Similar strings
    assert repo._similar_strings('cable', 'cables') == True
    
    # Different strings
    assert repo._similar_strings('cable', 'mouse') == False


def test_get_common_search_terms(no_results_test_csv):
    """Test extraction of common search terms"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    terms = repo._get_common_search_terms()
    
    # Should return a list of terms
    assert isinstance(terms, list)
    assert len(terms) > 0
    
    # Should contain meaningful terms from product names
    terms_lower = [t.lower() for t in terms]
    assert 'cable' in terms_lower or 'headphones' in terms_lower


def test_no_results_with_empty_query(no_results_test_csv):
    """Test suggestions with empty query"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    suggestions = repo.suggest_alternatives('')
    
    # Should still return structure
    assert 'popular_products' in suggestions
    assert 'similar_categories' in suggestions
    assert len(suggestions['similar_categories']) == 0


def test_popular_products_limit(no_results_test_csv):
    """Test that popular products respects limit parameter"""
    repo = CSVRepository(csv_path=no_results_test_csv)
    
    popular_2 = repo.get_popular_products(limit=2)
    popular_4 = repo.get_popular_products(limit=4)
    
    assert len(popular_2) == 2
    assert len(popular_4) == 4
