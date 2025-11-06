from fastapi import APIRouter, HTTPException
from ..repos.csv_repo import CSVRepository

router = APIRouter(prefix="/items", tags=["items"])

def get_csv_repo():
    return CSVRepository()

@router.get("/search")
def search_products(
    q: str = None,
    category: str = None,
    min_rating: float = None,
    max_price: float = None,
    page: int = 1,
    size: int = 10
):
    repo = get_csv_repo()
    offset = (page - 1) * size
    products = repo.search_products(
        query=q,
        category=category,
        min_rating=min_rating,
        max_price=max_price,
        limit=size,
        offset=offset
    )
    return {"products": products, "page": page, "size": size, "total": len(products)}

@router.get("/{product_id}")
def get_product_details(product_id: str):
    repo = get_csv_repo()
    product = repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    related = repo.get_related_products(product_id)
    return {
        "product": product,
        "related": related
    }

@router.get("/categories/list")
def get_categories():
    repo = get_csv_repo()
    return {"categories": repo.get_categories()}

