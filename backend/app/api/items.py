# Items API for viewing and searching items

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repos.item_repo import ItemRepo
from ..models.dto import ItemOut
from ..core.db import get_db

router = APIRouter(prefix="/items", tags=["items"])

def get_related_items(item, db):
	# Find related items (same category, exclude self, limit 4)
	return db.execute(
		db.query(type(item)).filter(
			type(item).category == item.category,
			type(item).id != item.id
		).limit(4)
	).scalars().all()

@router.get("/{item_id}", response_model=dict)
def get_item_details(item_id: int, db: Session = Depends(get_db)):
	repo = ItemRepo(db)
	item = repo.by_id(item_id)
	if not item:
		raise HTTPException(status_code=404, detail="Item not found")
	related = get_related_items(item, db)
	return {
		"item": ItemOut.model_validate(item),
		"related": [ItemOut.model_validate(r) for r in related]
	}
