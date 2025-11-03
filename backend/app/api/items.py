from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.dto import SearchQuery, ItemOut
from ..services.catalog_service import CatalogService
from ..core.db import get_db

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=list[ItemOut])
def search(q: str | None = None, category: str | None = None, available: bool | None = None,
           page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    svc = CatalogService(db)
    return svc.search(SearchQuery(q=q, category=category, available=available, page=page, size=size))

@router.get("/{item_id}", response_model=ItemOut)
def details(item_id: int, db: Session = Depends(get_db)):
    return CatalogService(db).details(item_id)

