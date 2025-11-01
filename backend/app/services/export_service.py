from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut
from ..repos.item_repo import ItemRepo

class ExportService:
    def __init__(self, db):
        self.repo = ItemRepo(db)

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        items = self.repo.get_many(req.ids)
        out = [ItemOut.model_validate(i) for i in items]
        return ExportPayload(count=len(out), items=out)

