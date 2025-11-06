from ..models.dto import ExportSelectionRequest, ExportPayload
from ..repos.csv_repo import CSVRepository

class ExportService:
    def __init__(self):
        self.repo = CSVRepository()

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        # Get products by IDs
        items = []
        for product_id in req.ids:
            product = self.repo.get_product_by_id(product_id)
            if product:
                items.append(product)
        return ExportPayload(count=len(items), items=items)

