from fastapi import APIRouter, HTTPException, Query
from ..services.places_service import get_place_autocomplete

router = APIRouter(prefix="/external", tags=["external"])

@router.get("/places/autocomplete")
def places_autocomplete(input: str = Query(..., min_length=1, description="Search query for place autocomplete")):
    try:
        predictions = get_place_autocomplete(input)
        return {"predictions": predictions}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error calling Google Places API: {str(e)}")

