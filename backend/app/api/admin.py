from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from ..models.dto import ItemCreate, ItemUpdate, ItemOut
from ..repos.item_repo import ItemRepo
from ..core.db import get_db
from ..core.errors import Forbidden
from ..core.security import is_admin_token

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(authorization: str | None = Header(default=None)):
    token = (authorization or "").split(" ")[-1]
    if not is_admin_token(token):
        raise Forbidden("Admin role required")

@router.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, _=Depends(require_admin), db: Session = Depends(get_db)):
    obj = ItemRepo(db).create(**payload.model_dump())
    return ItemOut.model_validate(obj)

@router.patch("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate, _=Depends(require_admin), db: Session = Depends(get_db)):
    obj = ItemRepo(db).update(item_id, **payload.model_dump())
    return ItemOut.model_validate(obj)

@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, _=Depends(require_admin), db: Session = Depends(get_db)):
    ItemRepo(db).delete(item_id)
    return None

