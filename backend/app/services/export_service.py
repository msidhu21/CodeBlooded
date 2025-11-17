from ..repos.item_repo import ItemRepo
from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut


class ExportService:
    def __init__(self, db=None):
        """
        db is kept for backwards compatibility with older tests
        that call ExportService(db=...). We don't actually use it.
        """
        self.repo = ItemRepo()

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        # Ask the repo for those items
        rows = self.repo.by_ids(req.ids)

        # Convert raw dicts/rows into ItemOut models
        items = [ItemOut.model_validate(r) for r in rows]

        return ExportPayload(count=len(items), items=items)
