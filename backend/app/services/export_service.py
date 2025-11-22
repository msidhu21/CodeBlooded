from ..repos.csv_repo import CSVRepository
from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut


class ExportService:
    def __init__(self, db=None):
        """
        db parameter kept for backwards compatibility with tests.
        Uses CSVRepository for actual data access.
        """
        self.repo = CSVRepository()

    def _ids_to_strings(self, ids):
        return [str(id) for id in ids]

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        str_ids = self._ids_to_strings(req.ids)
        rows = self.repo.get_products_by_ids(str_ids)

        # Convert raw dicts/rows into ItemOut models
        items = [ItemOut.model_validate(r) for r in rows]

        return ExportPayload(count=len(items), items=items)
