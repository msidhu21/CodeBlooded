from ..repos.csv_repo import CSVRepository
from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut


class ExportService:
    def __init__(self, db=None):
        """
        db parameter kept for backwards compatibility with tests.
        Uses CSVRepository for actual data access.
        """
        self.repo = CSVRepository()

    def _fetch_items(self, ids):
        str_ids = [str(id) for id in ids]
        return self.repo.get_products_by_ids(str_ids)

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        rows = self._fetch_items(req.ids)
        items = [ItemOut.model_validate(r) for r in rows]
        return ExportPayload(count=len(items), items=items)
