from ..repos.wishlist_repo import WishlistRepo
from ..repos.csv_repo import CSVRepository
from typing import List, Dict

class WishlistService:
    def __init__(self):
        self.wishlist_repo = WishlistRepo()
        self.product_repo = CSVRepository()
    
    def add_to_wishlist(self, user_id: int, product_id: str) -> Dict:
        item = self.wishlist_repo.add_to_wishlist(user_id, product_id)
        product = self.product_repo.get_product_by_id(product_id)
        if not product:
            from ..core.errors import NotFound
            raise NotFound("Product not found")
        return item
    
    def remove_from_wishlist(self, user_id: int, product_id: str) -> bool:
        return self.wishlist_repo.remove_from_wishlist(user_id, product_id)
    
    def get_user_wishlist(self, user_id: int) -> List[Dict]:
        product_ids = self.wishlist_repo.get_user_wishlist(user_id)
        if not product_ids:
            return []
        
        products = self.product_repo.get_products_by_ids(product_ids)
        return products
    
    def is_in_wishlist(self, user_id: int, product_id: str) -> bool:
        return self.wishlist_repo.is_in_wishlist(user_id, product_id)
    
    def get_wishlist_count(self, user_id: int) -> int:
        return self.wishlist_repo.get_wishlist_count(user_id)

