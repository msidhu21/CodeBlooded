import os

def get_google_places_api_key() -> str:
    key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not key:
        raise ValueError("GOOGLE_PLACES_API_KEY environment variable is not set")
    return key

