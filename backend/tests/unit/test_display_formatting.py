"""Unit tests for display formatting functionality"""
import pytest
import pandas as pd
from app.repos.csv_repo import CSVRepository


@pytest.fixture
def display_test_csv(tmp_path):
    """Create a test CSV with sample products"""
    test_data = pd.DataFrame({
        'product_id': ['D1', 'D2', 'D3'],
        'product_name': ['USB Cable', 'HDMI Cable', 'Power Adapter'],
        'category': ['Electronics|Cables', 'Electronics|Cables', 'Electronics|Adapters'],
        'discounted_price': ['₹299', '₹599', '₹899'],
        'actual_price': ['₹599', '₹999', '₹1,299'],
        'discount_percentage': ['50%', '40%', '31%'],
        'rating': [4.2, 4.5, 4.0],
        'rating_count': [1000, 500, 200],
        'about_product': ['Fast charging USB cable', 'High quality HDMI cable', 'Universal power adapter'],
        'user_id': ['U1', 'U2', 'U3'],
        'user_name': ['John', 'Jane', 'Bob'],
        'review_id': ['R1', 'R2', 'R3'],
        'review_title': ['Good', 'Great', 'Nice'],
        'review_content': ['Good product', 'Great product', 'Nice product'],
        'img_link': ['img1.jpg', 'img2.jpg', 'img3.jpg'],
        'product_link': ['link1', 'link2', 'link3']
    })
    
    csv_path = tmp_path / "display_products.csv"
    test_data.to_csv(csv_path, index=False)
    return str(csv_path)


def test_format_for_display_basic(display_test_csv):
    """Test basic display formatting without query"""
    repo = CSVRepository(csv_path=display_test_csv)
    products = repo.search_products(limit=3)
    
    formatted = repo.format_for_display(products)
    
    assert len(formatted) == 3
    # Check essential fields are present
    for product in formatted:
        assert 'product_id' in product
        assert 'product_name' in product
        assert 'discounted_price' in product
        assert 'actual_price' in product
        assert 'rating' in product
        assert 'img_link' in product
        assert 'product_link' in product
        assert 'about_product' in product  # Should have full description


def test_format_for_display_compact(display_test_csv):
    """Test compact display formatting"""
    repo = CSVRepository(csv_path=display_test_csv)
    products = repo.search_products(limit=3)
    
    formatted = repo.format_for_display(products, compact=True)
    
    assert len(formatted) == 3
    # Compact view should not include full description
    for product in formatted:
        assert 'about_product' not in product
        assert 'product_name' in product
        assert 'discounted_price' in product


def test_format_with_highlighting(display_test_csv):
    """Test search term highlighting"""
    repo = CSVRepository(csv_path=display_test_csv)
    products = repo.search_products(query='cable', limit=3)
    
    formatted = repo.format_for_display(products, query='cable')
    
    # Should return 2 products with "cable" in name
    assert len(formatted) == 2
    
    for product in formatted:
        assert 'highlighted_fields' in product
        # Cable products should have product_name highlighted
        if 'Cable' in product['product_name']:
            assert 'product_name' in product['highlighted_fields']


def test_highlight_multiple_fields(display_test_csv):
    """Test highlighting when query matches multiple fields"""
    repo = CSVRepository(csv_path=display_test_csv)
    
    # Search for "usb" which appears in name and description
    products = repo.search_products(query='usb', limit=3)
    formatted = repo.format_for_display(products, query='usb')
    
    if len(formatted) > 0:
        # USB cable should have multiple fields highlighted
        usb_product = formatted[0]
        assert 'highlighted_fields' in usb_product
        assert 'product_name' in usb_product['highlighted_fields']


def test_format_no_matches(display_test_csv):
    """Test formatting when no products match"""
    repo = CSVRepository(csv_path=display_test_csv)
    products = repo.search_products(query='nonexistent', limit=3)
    
    formatted = repo.format_for_display(products, query='nonexistent')
    
    assert len(formatted) == 0


def test_essential_fields_present(display_test_csv):
    """Test that all essential display fields are present"""
    repo = CSVRepository(csv_path=display_test_csv)
    products = repo.search_products(limit=1)
    
    formatted = repo.format_for_display(products)
    
    assert len(formatted) == 1
    product = formatted[0]
    
    # Essential fields for display
    essential_fields = [
        'product_id',
        'product_name',
        'category',
        'discounted_price',
        'actual_price',
        'discount_percentage',
        'rating',
        'rating_count',
        'img_link',
        'product_link'
    ]
    
    for field in essential_fields:
        assert field in product, f"Missing essential field: {field}"


def test_highlighting_case_insensitive(display_test_csv):
    """Test that highlighting is case-insensitive"""
    repo = CSVRepository(csv_path=display_test_csv)
    
    # Search with uppercase
    products = repo.search_products(query='USB', limit=3)
    formatted = repo.format_for_display(products, query='USB')
    
    if len(formatted) > 0:
        assert 'highlighted_fields' in formatted[0]
        assert len(formatted[0]['highlighted_fields']) > 0


def test_format_preserves_product_data(display_test_csv):
    """Test that formatting doesn't modify original product data"""
    repo = CSVRepository(csv_path=display_test_csv)
    products = repo.search_products(limit=1)
    
    original_name = products[0]['product_name']
    original_price = products[0]['discounted_price']
    
    formatted = repo.format_for_display(products, query='test')
    
    # Data should be preserved
    assert formatted[0]['product_name'] == original_name
    assert formatted[0]['discounted_price'] == original_price
