import asyncio
import httpx
import json
from typing import Dict, Any

async def test_search_api(query: str) -> Dict[str, Any]:
    """Test the search API with a given query."""
    url = "http://localhost:8010/api/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            print(f"\nSending POST request to {url}")
            print(f"Request body: {json.dumps({'query': query})}")
            
            response = await client.post(
                url,
                json={"query": query},
                headers=headers,
                timeout=30.0
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"Error response body: {response.text}")
                
            return response.json()
        except httpx.RequestError as e:
            print(f"Request error: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            print(f"Raw response: {response.text}")
            raise

async def run_tests():
    """Run a series of test queries."""
    test_queries = [
        "Find me a coffee shop in downtown Seattle",
        "What's the best Italian restaurant in New York City",
        "Show me parks near Central Park",
        "Where is the nearest gas station",
        "Find me a gym in San Francisco"
    ]
    
    print("\n=== Starting API Tests ===\n")
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        try:
            result = await test_search_api(query)
            print("\nResponse:")
            print(json.dumps(result, indent=2))
            
            if result.get("status") == "success":
                locations = result.get("locations", [])
                print(f"\nFound {len(locations)} locations")
                
                if locations:
                    print("\nFirst location details:")
                    first_location = locations[0]
                    print(f"Name: {first_location['name']}")
                    print(f"Address: {first_location['formatted_address']}")
                    print(f"Rating: {first_location.get('rating', 'N/A')}")
            else:
                print("\nError in response:", result.get("message", "Unknown error"))
                
        except Exception as e:
            print(f"\nError testing query: {str(e)}")
            import traceback
            print(traceback.format_exc())
        
        print("\n" + "="*50)

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the FastAPI server is running on http://localhost:8010")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    asyncio.run(run_tests()) 