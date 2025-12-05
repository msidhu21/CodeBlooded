from app.repos.cart_repo import CartRepo
from app.models.dto import CartItemAddRequest

class CartService:

    @staticmethod
    def add_item(request: CartItemAddRequest):
        CartRepo.add_item(request.user_id, request.product_id)
        return {"user_id": request.user_id, "product_id": request.product_id}

    @staticmethod
    def get_items(user_id: str):
        return CartRepo.get_items(user_id)

    @staticmethod
    def remove_item(request: CartItemAddRequest):
        CartRepo.remove_item(request.user_id, request.product_id)
        return {"message": "Item removed"}
