from fastapi import APIRouter, Header, HTTPException, Depends
from ..repos.csv_repo import CSVRepository
from ..core.errors import Forbidden
from ..core.security import is_admin_token

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

