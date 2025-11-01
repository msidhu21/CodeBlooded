from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..models.dto import ExportSelectionRequest
from ..services.export_service import ExportService
from ..core.db import get_db
from ..core.errors import Forbidden
from ..core.security import is_admin_token

router = APIRouter(prefix="/export", tags=["export"])

def require_admin(authorization: str | None = Header(default=None)):
    token = (authorization or "").split(" ")[-1]
    if not is_admin_token(token):
        raise Forbidden("Admin role required")

@router.post("/selection")
def export_selection(req: ExportSelectionRequest, _=Depends(require_admin), db: Session = Depends(get_db)):
    payload = ExportService(db).export_selection(req)
    return JSONResponse(
        content=payload.model_dump(),
        headers={"Content-Disposition": "attachment; filename=selection.json"}
    )

