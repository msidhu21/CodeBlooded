from fastapi import APIRouter, Header, HTTPException, Depends
from ..repos.csv_repo import CSVRepository
from ..repos.user_repo import UserRepo
from ..core.errors import Forbidden, NotFound
from ..core.security import is_admin_token
from pathlib import Path
import pandas as pd

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(authorization: str | None = Header(default=None)):
    token = (authorization or "").split(" ")[-1]
    if not is_admin_token(token):
        raise Forbidden("Admin role required")

def get_csv_repo():
    return CSVRepository()

@router.post("/items", status_code=201)
def create_item(payload: dict, _=Depends(require_admin)):
    repo = get_csv_repo()
    return repo.add_product(payload)

@router.patch("/items/{product_id}")
def update_item(product_id: str, payload: dict, _=Depends(require_admin)):
    repo = get_csv_repo()
    result = repo.update_product(product_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.delete("/items/{product_id}", status_code=204)
def delete_item(product_id: str, _=Depends(require_admin)):
    repo = get_csv_repo()
    if not repo.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return None


# New admin endpoints for user management and stats

@router.get("/users")
def get_all_users():
    """Get all users from CSV"""
    user_repo = UserRepo()
    users = user_repo.df.to_dict('records')
    return {"users": users}


@router.delete("/users/{email}")
def delete_user_by_email(email: str):
    """Delete a user by email"""
    user_repo = UserRepo()
    
    # Find user by email
    user_rows = user_repo.df[user_repo.df['email'] == email]
    if len(user_rows) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    user_repo.df = user_repo.df[user_repo.df['email'] != email]
    user_repo._save()
    
    return {"message": f"User {email} deleted successfully"}


@router.get("/wishlist/{email}")
def get_user_wishlist_stats(email: str):
    """Get wishlist stats for a specific user"""
    user_repo = UserRepo()
    
    # Find user
    user_rows = user_repo.df[user_repo.df['email'] == email]
    if len(user_rows) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = user_rows.iloc[0]['user_id']
    
    # Read wishlist CSV
    base_path = Path(__file__).parent.parent.parent
    wishlist_path = base_path / "data" / "wishlists.csv"
    
    try:
        wishlist_df = pd.read_csv(wishlist_path)
        user_wishlist = wishlist_df[wishlist_df['user_id'] == str(user_id)]
        
        items = user_wishlist['product_id'].tolist() if len(user_wishlist) > 0 else []
        
        return {
            "email": email,
            "user_id": user_id,
            "count": len(items),
            "items": items
        }
    except FileNotFoundError:
        return {
            "email": email,
            "user_id": user_id,
            "count": 0,
            "items": []
        }


@router.get("/stats")
def get_system_stats():
    """Get basic system statistics"""
    user_repo = UserRepo()
    
    # Get product count from CSV
    base_path = Path(__file__).parent.parent.parent
    products_path = base_path / "data" / "amazon.csv"
    
    try:
        products_df = pd.read_csv(products_path)
        product_count = len(products_df)
    except:
        product_count = 0
    
    return {
        "totalUsers": len(user_repo.df),
        "totalProducts": product_count,
        "activeUsers": len(user_repo.df[user_repo.df['role'] == 'user'])
    }
