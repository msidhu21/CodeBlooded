from ..models.dto import ExportSelectionRequest, ExportPayload, ItemOut
from ..repos.item_repo import ItemRepo
from ..core.errors import BadRequest

class ExportService:
    """Service for exporting selected items by their IDs."""
    
    def __init__(self, db):
        """Initialize the export service with a database connection.
        
        Args:
            db: Database connection/session
        """
        self.repo = ItemRepo(db)

    def _is_empty_request(self, ids: list) -> bool:
        """Check if the export request is empty.
        
        Args:
            ids: List of item IDs to check
            
        Returns:
            True if the list is empty, False otherwise
        """
        return not ids

    def _validate_ids(self, requested_ids: list, found_items: list) -> None:
        """Validate that all requested IDs exist in the found items.
        
        Args:
            requested_ids: List of IDs that were requested
            found_items: List of items found in the database
            
        Raises:
            BadRequest: If any requested IDs are missing from found_items
        """
        found_ids = {item.id for item in found_items}
        missing_ids = set(requested_ids) - found_ids
        if missing_ids:
            raise BadRequest(f"Items not found: {sorted(missing_ids)}")

    def _convert_items(self, items: list) -> list[ItemOut]:
        """Convert database items to output DTOs.
        
        Args:
            items: List of database item entities
            
        Returns:
            List of ItemOut DTOs
        """
        return [ItemOut.model_validate(item) for item in items]

    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        """Export selected items by their IDs.
        
        Args:
            req: Export request containing list of item IDs
            
        Returns:
            ExportPayload with count and list of exported items
            
        Raises:
            BadRequest: If any requested item IDs are not found
        """
        if self._is_empty_request(req.ids):
            return ExportPayload(count=0, items=[])
        
        items = self.repo.by_ids(req.ids)
        self._validate_ids(req.ids, items)
        out = self._convert_items(items)
        return ExportPayload(count=len(out), items=out)

