from app.repos.cart_repo import CartRepo
from app.repos.csv_repo import CSVRepository
from app.models.dto import CartItemAddRequest

class CartService:

    @staticmethod
    def add_item(request: CartItemAddRequest):
        CartRepo.add_item(request.user_id, request.product_id)
        return {"user_id": request.user_id, "product_id": request.product_id}

    @staticmethod
    def get_items(user_id: str):
        cart_items = CartRepo.get_items(user_id)
        
        # If cart is empty, return empty list
        if not cart_items:
            return []
        
        # Fetch full product details for each cart item
        csv_repo = CSVRepository()
        enriched_items = []
        
        for cart_item in cart_items:
            product_id = cart_item['product_id']
            product = csv_repo.get_product_by_id(product_id)
            
            if product:
                # Add quantity to the product object
                product['quantity'] = cart_item['quantity']
                enriched_items.append(product)
        
        return enriched_items

    @staticmethod
    def remove_item(request: CartItemAddRequest):
        CartRepo.remove_item(request.user_id, request.product_id)
        return {"message": "Item removed"}
