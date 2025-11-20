from fastapi import APIRouter, HTTPException
from ..repos.csv_repo import CSVRepository
import time
import math

router = APIRouter(prefix="/items", tags=["items"])

def get_csv_repo():
    return CSVRepository()

def clean_nan_values(data):
    """Replace NaN values with None for JSON serialization"""
    if isinstance(data, list):
        return [clean_nan_values(item) for item in data]
    elif isinstance(data, dict):
        return {key: clean_nan_values(value) for key, value in data.items()}
    elif isinstance(data, float) and math.isnan(data):
        return None
    return data

@router.get("/search")
def search_products(
    q: str = None,
    category: str = None,
    min_rating: float = None,
    max_rating: float = None,
    min_price: float = None,
    max_price: float = None,
    min_discount: float = None,
    page: int = 1,
    size: int = 10,
    compact: bool = False
):
    repo = get_csv_repo()
    offset = (page - 1) * size
    
    # Track search time for performance monitoring
    start_time = time.time()
    
    # Get results with total count
    products, total_results = repo.search_products(
        query=q,
        category=category,
        min_rating=min_rating,
        max_rating=max_rating,
        min_price=min_price,
        max_price=max_price,
        min_discount=min_discount,
        limit=size,
        offset=offset,
        return_total=True
    )
    
    # Format products for display with highlighting
    products = repo.format_for_display(products, query=q, compact=compact)
    
    search_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
    
    # Calculate pagination metadata
    total_pages = (total_results + size - 1) // size  # Ceiling division
    has_more = page < total_pages
    
    # Clean NaN values for JSON serialization
    products = clean_nan_values(products)
    
    return {
        "products": products,
        "pagination": {
            "page": page,
            "size": size,
            "total_results": total_results,
            "total_pages": total_pages,
            "has_more": has_more
        },
        "filters_applied": {
            "search_query": q,
            "category": category,
            "min_rating": min_rating,
            "max_rating": max_rating,
            "min_price": min_price,
            "max_price": max_price,
            "min_discount": min_discount
        },
        "meta": {
            "search_time_ms": search_time,
            "results_on_page": len(products)
        }
    }

@router.get("/{product_id}")
def get_product_details(product_id: str):
    repo = get_csv_repo()
    product = repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    related = repo.get_related_products(product_id)
    
    # Clean NaN values for JSON serialization
    product = clean_nan_values(product)
    related = clean_nan_values(related)
    
    return {
        "product": product,
        "related": related
    }

@router.get("/categories/list")
def get_categories():
    repo = get_csv_repo()
    return {"categories": repo.get_categories()}

