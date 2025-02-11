from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .models import SearchRequest, SearchResponse
from .services.claude_service import process_search_query
from .services.maps_service import search_places

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Google Maps Search API",
    description="API for searching locations using Google Maps and Claude",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {"status": "ok", "message": "API is running"}

@app.post("/api/search", response_model=SearchResponse)
async def search_location(request: SearchRequest) -> SearchResponse:
    """
    Search for locations using the provided query.
    
    Args:
        request: SearchRequest object containing the search query
        
    Returns:
        SearchResponse object containing the search results
    """
    logger.info(f"Received search request with query: {request.query}")
    
    try:
        # Process the query using Claude
        logger.info(f"Processing query with Claude: {request.query}")
        processed_query = await process_search_query(request.query)
        logger.info(f"Processed query: {processed_query}")
        
        # Search places using Google Maps
        logger.info(f"Searching Google Maps with processed query: {processed_query}")
        locations = await search_places(processed_query)
        logger.info(f"Found {len(locations)} locations")
        
        if not locations:
            return SearchResponse(
                status="success",
                message="No locations found",
                locations=[]
            )
        
        return SearchResponse(
            status="success",
            message="Locations found successfully",
            locations=locations
        )
        
    except Exception as e:
        logger.error(f"Error processing search request: {str(e)}", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) 