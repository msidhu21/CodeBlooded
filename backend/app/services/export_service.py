from ..repos.csv_repo import CSVRepository
from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut


class ExportService:
    def __init__(self, db=None):
        """
        db parameter kept for backwards compatibility with tests.
        Uses CSVRepository for actual data access.
        """
        self.repo = CSVRepository()

    def _prepare_ids(self, ids):
        return [str(id) for id in ids]

    def _to_item_models(self, rows):
        return [ItemOut.model_validate(r) for r in rows]

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        str_ids = self._prepare_ids(req.ids)
        rows = self.repo.get_products_by_ids(str_ids)

        items = self._to_item_models(rows)

        return ExportPayload(count=len(items), items=items)
