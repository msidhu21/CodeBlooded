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

@router.get("", response_model=list[CartItemResponse])
def get_cart(x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    user_id = get_user_id(x_user_id, authorization)
    return CartService.get_items(user_id)

@router.delete("/remove")
def remove_from_cart(product_id: str, x_user_id: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    user_id = get_user_id(x_user_id, authorization)
    request = CartItemAddRequest(user_id=user_id, product_id=product_id)
    return CartService.remove_item(request)

