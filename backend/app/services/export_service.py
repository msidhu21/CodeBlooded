from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut
from ..repos.item_repo import ItemRepo
from ..core.errors import BadRequest

class ExportService:
    def __init__(self, db):
        self.repo = ItemRepo(db)

    def _validate_ids(self, requested_ids, found_items):
        found_ids = {item.id for item in found_items}
        missing_ids = set(requested_ids) - found_ids
        if missing_ids:
            raise BadRequest(f"Items not found: {sorted(missing_ids)}")

    def _convert_items(self, items):
        return [ItemOut.model_validate(item) for item in items]

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        if not req.ids:
            return ExportPayload(count=0, items=[])
        
        items = self.repo.by_ids(req.ids)
        self._validate_ids(req.ids, items)
        out = self._convert_items(items)
        return ExportPayload(count=len(out), items=out)

