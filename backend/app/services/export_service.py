from ..repos.csv_repo import CSVRepository
from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut


class ExportService:
    def __init__(self, db=None):
        """
        db parameter kept for backwards compatibility with tests.
        Uses CSVRepository for actual data access.
        """
        self.repo = CSVRepository()

    def _validate_request(self, req: ExportSelectionRequest):
        if not req.ids:
            return ExportPayload(count=0, items=[])
        return None

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        rows = self._fetch_items(req.ids)

        # Convert raw dicts/rows into ItemOut models
        items = [ItemOut.model_validate(r) for r in rows]

        return ExportPayload(count=len(items), items=items)
