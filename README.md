# Google Maps Search with Anthropic Claude

A FastAPI application that combines Claude AI with Google Maps API to provide intelligent location search results. The application uses Claude to process natural language queries and returns relevant locations using Google Maps Places API.

## Features

- Natural language location search processing using Claude AI
- Google Maps Places API integration
- FastAPI backend with async support
- CORS enabled for frontend integration
- Proper error handling and logging
- Type-safe with Pydantic models
- User profile-based recommendations
- Location-aware contextual search

## Prerequisites

- Python 3.8+
- Google Maps API Key
- Anthropic API Key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/alinaqi/google-maps-anthropic.git
cd google-maps-anthropic
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Running the Application

1. Start the FastAPI server:
```bash
python src/run.py
```

2. The API will be available at `http://localhost:8010`

## API Endpoints

### POST /api/search

Search for locations using natural language queries.

#### Request

```json
{
    "query": "Find me a coffee shop in downtown Seattle"
}
```

#### Response

```json
{
    "status": "success",
    "message": "Locations found successfully",
    "locations": [
        {
            "name": "Example Coffee",
            "formatted_address": "123 Pike St, Seattle, WA 98101",
            "latitude": 47.123,
            "longitude": -122.456,
            "place_id": "abc123",
            "types": ["cafe", "food", "point_of_interest"],
            "rating": 4.5
        }
    ]
}
```

## User Profiles

The application supports different user profiles with specific interests:

1. Family with Young Children
   - Interests: schools, parks, family restaurants, playgrounds, pediatric clinics, supermarkets
   ```bash
   curl -X POST http://localhost:8010/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Find family-friendly restaurants near Dubai Marina"}'
   ```

2. Single Professional
   - Interests: gyms, cafes, restaurants, coworking spaces, entertainment
   ```bash
   curl -X POST http://localhost:8010/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Show me coworking spaces near Business Bay"}'
   ```

3. Family without Children
   - Interests: fine dining, shopping, cultural venues, fitness centers, date spots
   ```bash
   curl -X POST http://localhost:8010/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Find romantic restaurants near Palm Jumeirah"}'
   ```

4. Senior Citizens
   - Interests: medical facilities, parks, community centers, quiet restaurants, pharmacies
   ```bash
   curl -X POST http://localhost:8010/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Show me medical facilities near Dubai Healthcare City"}'
   ```

## Dubai-Specific Examples

Here are some Dubai-specific location queries you can try:

1. Area Exploration:
```bash
curl -X POST http://localhost:8010/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Find points of interest near Dubai Marina"}'
```

2. Restaurant Search:
```bash
curl -X POST http://localhost:8010/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best restaurants near Palm Jumeirah?"}'
```

3. Family-Friendly Locations:
```bash
curl -X POST http://localhost:8010/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me schools and parks near Downtown Dubai"}'
```

### Sample Dubai Output

```json
{
  "status": "success",
  "message": "Locations found successfully",
  "locations": [
    {
      "name": "Dubai Marina Mall",
      "formatted_address": "Sheikh Zayed Road, Dubai Marina, Dubai, United Arab Emirates",
      "latitude": 25.0771,
      "longitude": 55.1401,
      "place_id": "ChIJB1zIXNxt4zsRHc_U_ZWrGQE",
      "types": [
        "shopping_mall",
        "point_of_interest",
        "establishment"
      ],
      "rating": 4.4
    }
  ]
}
```

## Development

- The application uses FastAPI's automatic API documentation
- Visit `http://localhost:8010/docs` for interactive API documentation
- Visit `http://localhost:8010/redoc` for alternative API documentation

## Testing

Run the test script to verify the API functionality:
```bash
python src/test_api.py
```

The test script includes:
- General location queries
- Profile-specific queries
- Dubai-specific location tests
- Different user demographic scenarios

## Error Handling

The API includes comprehensive error handling:
- Invalid queries return appropriate error messages
- API timeouts are handled gracefully
- Rate limiting is respected for both Claude and Google Maps APIs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 