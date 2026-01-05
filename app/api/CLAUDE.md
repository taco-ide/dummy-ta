# CLAUDE.md - API Module Context

## Overview

The `api/` directory contains all HTTP endpoint definitions organized by API version.

## Directory Structure

```
api/
├── __init__.py
└── v1/                  # Version 1 endpoints
    ├── __init__.py
    └── chat_endpoints.py
```

## API Versioning

The API uses URL-based versioning (`/api/v1/`, `/api/v2/`, etc.) to support:
- Backward compatibility for existing clients
- Gradual migration to new API versions
- Clear deprecation paths

## Current Endpoints (v1)

### POST /api/v1/chat
Main chat endpoint for interacting with the LLM.

**Request Schema (ChatRequest):**
```python
{
    "prompt": str,           # Required: User's input message
    "system_message": str    # Optional: Custom system prompt
}
```

**Response Schema (ChatResponse):**
```python
{
    "response": str          # Model's generated response
}
```

## Development Guidelines

### Adding New Endpoints

1. Create a new file in `v1/` directory for new functionality
2. Define Pydantic models for request/response validation
3. Create an `APIRouter` with appropriate tags
4. Include the router in `main.py`

### Pydantic Models
- Use `Field()` for documentation and validation
- Provide clear descriptions for Swagger UI
- Use `Optional[]` for non-required fields
- Define default values where appropriate

### Example Pattern

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.some_service import SomeService
from app.core.logger import logger

router = APIRouter(tags=["Feature Name"])

class MyRequest(BaseModel):
    field: str = Field(..., description="Field description")

class MyResponse(BaseModel):
    result: str = Field(..., description="Result description")

@router.post("/endpoint", response_model=MyResponse)
async def my_endpoint(request: MyRequest):
    """Endpoint docstring for Swagger UI."""
    try:
        # Business logic
        return MyResponse(result="...")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error message")
```

## Error Handling

- Return `HTTPException` with appropriate status codes
- 400: Bad Request (invalid input)
- 404: Not Found
- 500: Internal Server Error
- Always log errors before raising exceptions
