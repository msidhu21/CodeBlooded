from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut
from ..repos.item_repo import ItemRepo

class ExportService:
    def __init__(self, repo: ItemRepo):
        self.repo = repo

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        items = self.repo.get_many(req.ids)
        pojos = [ItemOut.model_validate(i) for i in items]
        return ExportPayload(count=len(pojos), items=pojos)

