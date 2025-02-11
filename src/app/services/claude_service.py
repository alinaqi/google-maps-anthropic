import anthropic
from ..config import get_settings

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)



async def process_search_query(query: str) -> str:
    """
    Process the search query using Claude to extract location information.
    
    Args:
        query: User's search query
        
    Returns:
        Processed query optimized for Google Maps search
    """
    prompt = f"""Given the following location search query, please analyze it and return a clear, 
    specific location search query that would work well with Google Maps. Focus on the key location 
    details and remove any unnecessary information. Only return the processed query, nothing else.

    Original query: {query}
    """
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8096,
        temperature=0,
        system="You are a world-class poet. Respond only with short poems.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    return message.content 