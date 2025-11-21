from ..repos.item_repo import ItemRepo
from ..models.dto import ExportSelectionRequest, ExportPayload


class ExportService:
    def __init__(self, db=None, repo: ItemRepo | None = None):
        """
        `db` is kept for backwards compatibility with older code/tests that
        call ExportService(db=...). For unit tests, they usually inject a fake
        repo by assigning to `svc.repo` directly, or pass `repo=...`.
        """
        self.repo = repo or ItemRepo(db)

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """
        Export selected items by their IDs.
        """
        if not req.ids:
            return ExportPayload(count=0, items=[])

        rows = self.repo.get_many(req.ids)
        return ExportPayload(count=len(rows), items=rows)
