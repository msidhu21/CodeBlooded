from fastapi import APIRouter, Header, HTTPException, Depends
from ..repos.csv_repo import CSVRepository
from ..repos.user_repo import UserRepo
from ..core.errors import Forbidden, NotFound
from ..core.security import is_admin_token
from pathlib import Path
import pandas as pd
import math

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(authorization: str | None = Header(default=None)):
    token = (authorization or "").split(" ")[-1]
    if not is_admin_token(token):
        raise Forbidden("Admin role required")

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
    users = clean_nan_values(users)
    return {"users": users}


@router.get("/users/search/{email}")
def search_user_by_email(email: str):
    """Search for a user by email"""
    user_repo = UserRepo()
    
    # Find user by email (case-insensitive partial match)
    user_rows = user_repo.df[user_repo.df['email'].str.contains(email, case=False, na=False)]
    
    if len(user_rows) == 0:
        return {"user": None, "message": "User not found"}
    
    # Return first matching user with cleaned NaN values
    user = user_rows.iloc[0].to_dict()
    user = clean_nan_values(user)
    return {"user": user}


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
    """Get comprehensive system statistics"""
    user_repo = UserRepo()
    
    # Get product count from CSV
    base_path = Path(__file__).parent.parent.parent
    products_path = base_path / "data" / "amazon.csv"
    cart_path = base_path / "data" / "cart.csv"
    wishlist_path = base_path / "data" / "wishlists.csv"
    
    try:
        products_df = pd.read_csv(products_path)
        product_count = len(products_df)
        categories = products_df['category'].nunique() if 'category' in products_df.columns else 0
    except:
        product_count = 0
        categories = 0
    
    # Get cart statistics
    try:
        cart_df = pd.read_csv(cart_path)
        total_cart_items = len(cart_df)
        users_with_carts = cart_df['user_id'].nunique() if len(cart_df) > 0 else 0
    except:
        total_cart_items = 0
        users_with_carts = 0
    
    # Get wishlist statistics
    try:
        wishlist_df = pd.read_csv(wishlist_path)
        total_wishlist_items = len(wishlist_df)
        users_with_wishlists = wishlist_df['user_id'].nunique() if len(wishlist_df) > 0 else 0
    except:
        total_wishlist_items = 0
        users_with_wishlists = 0
    
    return {
        "totalUsers": len(user_repo.df),
        "totalProducts": product_count,
        "activeUsers": len(user_repo.df[user_repo.df['role'] == 'user']),
        "totalCategories": categories,
        "cartStats": {
            "totalItems": total_cart_items,
            "usersWithCarts": users_with_carts
        },
        "wishlistStats": {
            "totalItems": total_wishlist_items,
            "usersWithWishlists": users_with_wishlists
        }
    }


@router.get("/recent-users")
def get_recent_users():
    """Get list of recent user registrations"""
    user_repo = UserRepo()
    
    # Sort by user_id (assuming higher IDs are more recent)
    users = user_repo.df.sort_values('user_id', ascending=False).head(10).to_dict('records')
    users = clean_nan_values(users)
    
    return {"recent_users": users}


@router.get("/health")
def get_system_health():
    """Get system health status"""
    import os
    import time
    
    base_path = Path(__file__).parent.parent.parent
    health = {
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {}
    }
    
    # Check if data files exist and are accessible
    files_to_check = {
        "users_db": base_path / "data" / "users.csv",
        "products_db": base_path / "data" / "amazon.csv",
        "cart_db": base_path / "data" / "cart.csv",
        "wishlist_db": base_path / "data" / "wishlists.csv"
    }
    
    all_healthy = True
    for name, file_path in files_to_check.items():
        if file_path.exists():
            try:
                # Try to read the file
                df = pd.read_csv(file_path)
                health["checks"][name] = {
                    "status": "healthy",
                    "records": len(df),
                    "size_kb": round(os.path.getsize(file_path) / 1024, 2)
                }
            except Exception as e:
                health["checks"][name] = {
                    "status": "error",
                    "error": str(e)
                }
                all_healthy = False
        else:
            health["checks"][name] = {
                "status": "missing",
                "error": "File not found"
            }
            all_healthy = False
    
    # Overall status
    health["status"] = "healthy" if all_healthy else "degraded"
    
    return health
