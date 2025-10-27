from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..models.dto import ExportSelectionRequest
from ..repos.item_repo import ItemRepo
from ..services.export_service import ExportService
from ..core.deps import get_db, require_admin  # keep admin-only for demo

router = APIRouter(prefix="/export", tags=["export"])

@router.post("/selection")
def export_selection(req: ExportSelectionRequest,
                     _admin = Depends(require_admin),
                     db: Session = Depends(get_db)):
    service = ExportService(ItemRepo(db))
    payload = service.export_selection(req)
    return JSONResponse(
        content=payload.model_dump(),
        headers={"Content-Disposition": "attachment; filename=selection.json"}
    )

