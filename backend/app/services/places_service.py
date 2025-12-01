import httpx
from ..core.config import get_google_places_api_key

GOOGLE_PLACES_AUTOCOMPLETE_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"

def get_place_autocomplete(input_text: str) -> list[dict]:
    if not input_text or not input_text.strip():
        return []
    
    api_key = get_google_places_api_key()
    
    params = {
        "input": input_text.strip(),
        "key": api_key,
        "components": "country:ca"
    }
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(GOOGLE_PLACES_AUTOCOMPLETE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK" and data.get("status") != "ZERO_RESULTS":
                error_message = data.get("error_message", "Unknown error from Google Places API")
                raise Exception(f"Google Places API error: {error_message}")
            
            predictions = data.get("predictions", [])
            return [
                {
                    "description": pred.get("description", ""),
                    "place_id": pred.get("place_id", "")
                }
                for pred in predictions
            ]
    except httpx.HTTPError as e:
        raise Exception(f"Network error calling Google Places API: {str(e)}")
    except Exception as e:
        raise

