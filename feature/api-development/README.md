# Branch: feature/api-development

## Purpose
Build REST API with FastAPI to serve recommendations.

## Files
- `app.py` - FastAPI application
- `static/index.html` - Web interface
- `tests/test_api.py` - API tests
- `tests/test_integration.py` - Integration tests
- `requirements.txt` - Updated dependencies
- `README.md` - This file

## Key Features
- Multiple endpoints (recommend, health, metrics)
- Prometheus metrics collection
- CORS support for web interface
- Interactive web UI for demonstrations
- Error handling and validation

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app:app --reload

# Run tests
pytest tests/test_api.py
pytest tests/test_integration.py
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /predict` - Get recommendations for a user
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /metrics` - Prometheus metrics endpoint

## Testing
Run tests with:
```bash
pytest tests/ -v
```

