from sqlalchemy.orm import Session
from ..repos.item_repo import ItemRepo
from ..models.dto import SearchQuery, ItemOut

class CatalogService:
    def __init__(self, db: Session):
        self.repo = ItemRepo(db)

    def search(self, q: SearchQuery) -> list[ItemOut]:
        items = self.repo.search(q=q.q, category=q.category, available=q.available, page=q.page, size=q.size)
        return [ItemOut.model_validate(i) for i in items]

    def details(self, item_id: int) -> ItemOut:
        i = self.repo.by_id(item_id)
        return ItemOut.model_validate(i)

