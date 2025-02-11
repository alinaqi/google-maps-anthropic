from pydantic import BaseModel
from typing import List, Optional


class Location(BaseModel):
    """Location model with coordinates and place details."""
    
    name: str
    formatted_address: str
    latitude: float
    longitude: float
    place_id: str
    types: List[str]
    rating: Optional[float] = None


class SearchRequest(BaseModel):
    """Search request model."""
    
    query: str


class SearchResponse(BaseModel):
    """Search response model."""
    
    status: str = "success"
    message: str
    locations: List[Location] 