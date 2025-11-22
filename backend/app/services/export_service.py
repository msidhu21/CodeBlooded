from ..repos.csv_repo import CSVRepository
from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut


class ExportService:
    def __init__(self, db=None, repo=None):
        """
        db parameter kept for backwards compatibility with tests.
        Uses CSVRepository for actual data access.
        repo parameter allows tests to inject fake repositories.
        """
        self.repo = repo or CSVRepository()

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        # Ask the repo for those items - convert int ids to string for CSV
        str_ids = [str(id) for id in req.ids]
        rows = self.repo.get_products_by_ids(str_ids)

        # Convert raw dicts/rows into ItemOut models
        items = [ItemOut.model_validate(r) for r in rows]

        return ExportPayload(count=len(items), items=items)
