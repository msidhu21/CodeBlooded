from fastapi import APIRouter, HTTPException
from app.services.cart_service import CartService
from app.models.dto import CartItemAddRequest, CartItemResponse

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/add", response_model=CartItemResponse)
def add_to_cart(request: CartItemAddRequest):
    return CartService.add_item(request)

@router.get("/{user_id}", response_model=list[CartItemResponse])
def get_cart(user_id: str):
    return CartService.get_items(user_id)

@router.delete("/remove", response_model=dict)
def remove_from_cart(request: CartItemAddRequest):
    return CartService.remove_item(request)

