from fastapi import APIRouter, HTTPException, Header
from app.services.cart_service import CartService
from app.models.dto import CartItemAddRequest, CartItemResponse

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_user_id(x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)) -> str:
    """
    Extract user_id from X-User-Id header or authorization header.
    Falls back to "1" if not provided.
    """
    if x_user_id:
        return x_user_id
    
    # Future: decode JWT from authorization header
    if authorization and authorization.startswith("Bearer "):
        pass
    
    return "1"

@router.post("/add", response_model=CartItemResponse)
def add_to_cart(product_id: str, x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    user_id = get_user_id(x_user_id, authorization)
    request = CartItemAddRequest(user_id=user_id, product_id=product_id)
    return CartService.add_item(request)

@router.get("")
def get_cart(x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    user_id = get_user_id(x_user_id, authorization)
    return CartService.get_items(user_id)

@router.get("/{product_id}/check")
def check_cart(product_id: str, x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    user_id = get_user_id(x_user_id, authorization)
    items = CartService.get_items(user_id)
    # Handle both dict and object responses
    is_in_cart = any(
        (item.product_id if hasattr(item, 'product_id') else item['product_id']) == product_id 
        for item in items
    )
    return {"is_in_cart": is_in_cart}

@router.delete("/remove")
def remove_from_cart(product_id: str, x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    user_id = get_user_id(x_user_id, authorization)
    request = CartItemAddRequest(user_id=user_id, product_id=product_id)
    return CartService.remove_item(request)

