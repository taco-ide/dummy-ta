# CLAUDE.md - App Module Context

## Overview

The `app/` directory is the main Python package containing all application code for the dummy-ta Teaching Assistant API.

## Directory Structure

```
app/
├── __init__.py          # Package initializer
├── main.py              # FastAPI application entry point
├── api/                 # API layer (endpoints, routing)
│   └── v1/              # Version 1 of the API
├── core/                # Core utilities (config, logging)
└── services/            # Business logic layer
```

## Key Components

### main.py
- FastAPI application initialization with lifespan context manager
- HTTP middleware for request/response logging
- Router inclusion with `/api/v1` prefix
- Root endpoint for health checks

### Architecture Pattern
The application follows a layered architecture:
1. **API Layer** (`api/`): HTTP endpoint definitions and request/response models
2. **Service Layer** (`services/`): Business logic and external integrations (LLM)
3. **Core Layer** (`core/`): Cross-cutting concerns (configuration, logging)

## Development Guidelines

### Adding New Endpoints
1. Create endpoint function in appropriate `api/v1/` module
2. Define Pydantic request/response models
3. Implement business logic in `services/` module
4. Use `logger` from `core.logger` for logging
5. Access settings via `get_settings()` from `core.settings`

### Error Handling
- Use `HTTPException` for API errors with appropriate status codes
- Log errors with `exc_info=True` for stack traces
- Return user-friendly error messages, not internal details

### Async/Await
- All FastAPI endpoints should be `async def`
- Use async middleware pattern for cross-cutting concerns

## Import Patterns

```python
from app.api.v1.chat_endpoints import router as chat_router
from app.services.chat_service import ChatService
from app.core.settings import get_settings
from app.core.logger import logger
```

## Testing

Run the application locally:
```bash
poetry run uvicorn app.main:app --reload
```

Access Swagger UI at `http://localhost:8000/docs`
