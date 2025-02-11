import httpx
from typing import List
from ..models import Location
from ..config import get_settings

settings = get_settings()


async def search_places(query: str) -> List[Location]:
    """
    Search places using Google Maps Places API.
    
    Args:
        query: Search query string
        
    Returns:
        List of Location objects
    """
    async with httpx.AsyncClient() as client:
        # First, use Places API to search for places
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": query,
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        response = await client.get(search_url, params=params)
        data = response.json()
        
        if data["status"] != "OK":
            return []
        
        locations = []
        for result in data["results"][:5]:  # Limit to top 5 results
            location = Location(
                name=result["name"],
                formatted_address=result["formatted_address"],
                latitude=result["geometry"]["location"]["lat"],
                longitude=result["geometry"]["location"]["lng"],
                place_id=result["place_id"],
                types=result["types"],
                rating=result.get("rating")
            )
            locations.append(location)
            
        return locations 