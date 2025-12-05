from fastapi import APIRouter, HTTPException, Header
from ..services.wishlist_service import WishlistService
from ..models.dto import WishlistResponse
from ..core.errors import NotFound
import math

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

def get_user_id(authorization: str | None = None) -> int:
    return 1

@router.post("/{product_id}")
def add_to_wishlist(product_id: str, authorization: str | None = Header(default=None)):
    user_id = get_user_id(authorization)
    try:
        service = WishlistService()
        item = service.add_to_wishlist(user_id, product_id)
        return {"message": "Item added to wishlist", "item": item}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add item: {str(e)}")

@router.delete("/{product_id}")
def remove_from_wishlist(product_id: str, authorization: str | None = Header(default=None)):
    user_id = get_user_id(authorization)
    service = WishlistService()
    success = service.remove_from_wishlist(user_id, product_id)
    if success:
        return {"message": "Item removed from wishlist"}
    raise HTTPException(status_code=404, detail="Item not found in wishlist")

@router.get("", response_model=WishlistResponse)
def get_wishlist(authorization: str | None = Header(default=None)):
    user_id = get_user_id(authorization)
    service = WishlistService()
    products = service.get_user_wishlist(user_id)
    return {
        "products": products,
        "count": len(products)
    }

@router.get("/{product_id}/check")
def check_wishlist(product_id: str, authorization: str | None = Header(default=None)):
    user_id = get_user_id(authorization)
    service = WishlistService()
    is_in = service.is_in_wishlist(user_id, product_id)
    return {"is_in_wishlist": is_in}

@router.get("/count")
def get_wishlist_count(authorization: str | None = Header(default=None)):
    user_id = get_user_id(authorization)
    service = WishlistService()
    count = service.get_wishlist_count(user_id)
    return {"count": count}

