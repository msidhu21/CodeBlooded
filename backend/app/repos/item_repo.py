from typing import Iterable, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.entities import Item
from ..core.errors import NotFound, Conflict

class ItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_id(self, item_id: int) -> Item:
        obj = self.db.get(Item, item_id)
        if not obj:
            raise NotFound("Item not found")
        return obj

    def by_sku(self, sku: str) -> Optional[Item]:
        return self.db.execute(select(Item).where(Item.sku == sku)).scalars().first()

    def create(self, *, sku: str, name: str, category: str, available: bool, description: str) -> Item:
        if self.by_sku(sku):
            raise Conflict("Duplicate SKU")
        obj = Item(sku=sku, name=name, category=category, available=available, description=description)
        self.db.add(obj)
        self.db.flush()  # obtain PK
        return obj

    def update(self, item_id: int, **fields) -> Item:
        obj = self.by_id(item_id)
        for k, v in fields.items():
            if v is not None:
                setattr(obj, k, v)
        self.db.flush()
        return obj

    def delete(self, item_id: int) -> None:
        obj = self.by_id(item_id)
        self.db.delete(obj)
        self.db.flush()

    def get_many(self, ids: Iterable[int]) -> List[Item]:
        if not ids:
            return []
        stmt = select(Item).where(Item.id.in_(list(ids)))
        return list(self.db.execute(stmt).scalars())

