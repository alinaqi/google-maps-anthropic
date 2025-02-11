import asyncio
import httpx
import json
from typing import Dict, Any, List, Tuple

class UserProfile:
    """User profile with preferences based on demographics."""
    
    def __init__(self, name: str, description: str, interests: List[str]):
        self.name = name
        self.description = description
        self.interests = interests

# Define user profiles
USER_PROFILES = {
    "family_with_kids": UserProfile(
        "Family with Young Children",
        "Parents with children under 12",
        ["schools", "parks", "family restaurants", "playgrounds", "pediatric clinics", "supermarkets"]
    ),
    "single_professional": UserProfile(
        "Single Professional",
        "Young professional in their 20s-30s",
        ["gyms", "cafes", "restaurants", "coworking spaces", "entertainment"]
    ),
    "family_no_kids": UserProfile(
        "Family without Children",
        "Married couple or partners without children",
        ["fine dining", "shopping", "cultural venues", "fitness centers", "date spots"]
    ),
    "senior_citizens": UserProfile(
        "Senior Citizens",
        "Retired individuals or elderly couples",
        ["medical facilities", "parks", "community centers", "quiet restaurants", "pharmacies"]
    )
}

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

def get_dubai_queries() -> List[Tuple[str, str]]:
    """Get Dubai-specific test queries with descriptions."""
    return [
        (
            "Find points of interest near Dubai Marina",
            "General area exploration"
        ),
        (
            "What are the best restaurants near Palm Jumeirah?",
            "Restaurant search"
        ),
        (
            "Show me schools and parks near Downtown Dubai",
            "Family-friendly locations"
        ),
        (
            "Find medical facilities and pharmacies near Dubai Healthcare City",
            "Healthcare facilities"
        ),
        (
            "What entertainment options are available near Dubai Mall?",
            "Entertainment venues"
        )
    ]

def get_profile_specific_queries(profile: UserProfile, location: str) -> List[str]:
    """Generate queries based on user profile and location."""
    return [
        f"Find {interest} near {location}" for interest in profile.interests
    ]

async def run_tests():
    """Run a series of test queries."""
    # Test general Dubai queries
    print("\n=== Testing General Dubai Queries ===\n")
    dubai_queries = get_dubai_queries()
    for query, description in dubai_queries:
        print(f"\nTesting {description}")
        print(f"Query: '{query}'")
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
    
    # Test profile-specific queries
    dubai_locations = [
        "Dubai Marina",
        "Downtown Dubai",
        "Palm Jumeirah",
        "JBR",
        "Business Bay"
    ]
    
    for profile_id, profile in USER_PROFILES.items():
        print(f"\n=== Testing Queries for {profile.name} ===")
        print(f"Profile Description: {profile.description}")
        print(f"Interests: {', '.join(profile.interests)}")
        
        # Test for each Dubai location
        for location in dubai_locations:
            queries = get_profile_specific_queries(profile, location)
            for query in queries[:2]:  # Test first 2 interests per location to keep output manageable
                print(f"\nTesting query: '{query}'")
                try:
                    result = await test_search_api(query)
                    print("\nResponse:")
                    print(json.dumps(result, indent=2))
                    
                    if result.get("status") == "success":
                        locations = result.get("locations", [])
                        print(f"\nFound {len(locations)} locations")
                        
                        if locations:
                            print("\nTop 3 locations:")
                            for idx, loc in enumerate(locations[:3], 1):
                                print(f"\n{idx}. {loc['name']}")
                                print(f"   Address: {loc['formatted_address']}")
                                print(f"   Rating: {loc.get('rating', 'N/A')}")
                                print(f"   Types: {', '.join(loc['types'])}")
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