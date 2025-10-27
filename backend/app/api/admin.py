from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.dto import ItemCreate, ItemUpdate, ItemOut
from ..repos.item_repo import ItemRepo
from ..core.deps import get_db, require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate,
                _admin = Depends(require_admin),
                db: Session = Depends(get_db)):
    repo = ItemRepo(db)
    item = repo.create(**payload.model_dump())
    return ItemOut.model_validate(item)

@router.patch("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int,
                payload: ItemUpdate,
                _admin = Depends(require_admin),
                db: Session = Depends(get_db)):
    repo = ItemRepo(db)
    item = repo.update(item_id, **payload.model_dump())
    return ItemOut.model_validate(item)

@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int,
                _admin = Depends(require_admin),
                db: Session = Depends(get_db)):
    repo = ItemRepo(db)
    repo.delete(item_id)
    return None

