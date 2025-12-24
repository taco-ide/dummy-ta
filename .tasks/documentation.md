# Comprehensive Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Deep Dive](#architecture-deep-dive)
3. [Component Analysis](#component-analysis)
4. [Configuration System](#configuration-system)
5. [API Reference](#api-reference)
6. [Deployment Options](#deployment-options)
7. [Development Workflow](#development-workflow)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Known Issues and Limitations](#known-issues-and-limitations)
10. [Future Improvements](#future-improvements)

---

## Project Overview

### Purpose

**dummy-ta** is a Teaching Assistant (TA) API implementation built to assist undergraduate students in learning Python programming. The name "TACO Assistant" (Teaching Assistant COde) reflects its educational purpose.

### Core Functionality

The application provides a REST API that accepts natural language prompts and returns AI-generated responses using a locally-hosted Large Language Model (LLM). This enables:

- Interactive coding Q&A
- Python concept explanations
- Code review and suggestions
- Learning guidance

### Technology Choices Rationale

| Technology | Reason |
|------------|--------|
| **FastAPI** | Modern async framework with automatic OpenAPI documentation, type validation via Pydantic, and high performance |
| **llama-cpp-python** | Enables running LLMs locally without cloud dependencies, supporting various quantized GGUF models |
| **Hugging Face Hub** | Provides easy access to pre-trained models with automatic downloading and caching |
| **Poetry** | Modern dependency management with lock files for reproducible builds |
| **Docker** | Consistent deployment environment across development and production |

---

## Architecture Deep Dive

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Client (curl, browser)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Middleware Layer                      │   │
│  │            (Request/Response Logging)                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   API Layer                          │   │
│  │              (app/api/v1/endpoints)                  │   │
│  │         - Request validation (Pydantic)              │   │
│  │         - Response formatting                        │   │
│  │         - Error handling                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Service Layer                        │   │
│  │               (app/services/)                        │   │
│  │         - Business logic                             │   │
│  │         - LLM interaction                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Core Layer                          │   │
│  │                (app/core/)                           │   │
│  │         - Configuration (settings.py)                │   │
│  │         - Logging (logger.py)                        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    llama-cpp-python                          │
│               (Local LLM Inference Engine)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GGUF Model File                           │
│              (Downloaded from Hugging Face)                  │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **Client Request** → HTTP POST to `/api/v1/chat`
2. **Middleware** → Logs incoming request method and URL
3. **Router** → Routes to `chat` endpoint function
4. **Pydantic Validation** → Validates `ChatRequest` model
5. **Service Call** → `ChatService.generate_response()` invoked
6. **LLM Processing** → Messages formatted and sent to llama.cpp
7. **Response Generation** → Model generates completion
8. **Response Formatting** → Wrapped in `ChatResponse` model
9. **Middleware** → Logs response status code
10. **Client Response** → JSON response returned

### Lifespan Management

The application uses FastAPI's lifespan context manager pattern:

```python
@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup: Initialize resources
    logger.info("Starting up the FastAPI application")
    yield
    # Shutdown: Cleanup resources
    logger.info("Shutting down the FastAPI application")
```

This pattern ensures proper initialization and cleanup of resources.

---

## Component Analysis

### main.py - Application Entry Point

**Location:** `app/main.py`

**Responsibilities:**
- FastAPI app initialization
- Router registration with version prefix
- HTTP middleware for logging
- Root health check endpoint

**Key Implementation Details:**

```python
# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting up the FastAPI application")
    yield
    logger.info("Shutting down the FastAPI application")

# Middleware logs all requests/responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
```

### chat_endpoints.py - API Definitions

**Location:** `app/api/v1/chat_endpoints.py`

**Components:**

1. **Message Model** - For multi-turn conversations (currently unused)
2. **ChatRequest Model** - Input validation
3. **ChatResponse Model** - Output structure
4. **chat() Endpoint** - Main chat handler

**Request/Response Schema:**

```python
class ChatRequest(BaseModel):
    prompt: str = Field(..., description="The user's input message")
    system_message: Optional[str] = Field(
        default=None,
        description="Optional custom system message"
    )

class ChatResponse(BaseModel):
    response: str = Field(..., description="The model's response")
```

### chat_service.py - LLM Integration

**Location:** `app/services/chat_service.py`

**Key Features:**

1. **Model Initialization:**
   - Downloads model from HuggingFace on first run
   - Configurable GPU layer offloading
   - Configurable context window size

2. **Chat Completion:**
   - Formats messages in OpenAI-compatible format
   - Uses system message for behavior control
   - Configurable temperature and max tokens

**Model Loading:**

```python
self.llm = Llama.from_pretrained(
    repo_id=config.MODEL_REPO_ID,        # HuggingFace repo
    filename=config.MODEL_FILENAME,       # GGUF file pattern
    n_gpu_layers=config.MODEL_GPU_LAYERS, # GPU offloading
    n_ctx=config.MODEL_CONTEXT_WINDOW,    # Context size
)
```

### settings.py - Configuration Management

**Location:** `app/core/settings.py`

**Design Pattern:** Singleton-like configuration class with environment variable loading.

**Configuration Categories:**

| Category | Variables |
|----------|-----------|
| Model | `MODEL_REPO_ID`, `MODEL_FILENAME`, `MODEL_GPU_LAYERS`, `MODEL_CONTEXT_WINDOW`, `MODEL_MAX_TOKENS` |
| Chat | `CHAT_TEMPERATURE`, `SYSTEM_MESSAGE` |
| Runtime | `USE_GPU` |

### logger.py - Logging Configuration

**Location:** `app/core/logger.py`

**Configuration:**
- Logger name: `dummy_ta`
- Default level: DEBUG
- Output: Console (StreamHandler)
- Format: `%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s`

---

## Configuration System

### Environment Variables

All configuration is managed through environment variables loaded from a `.env` file.

**Template File:** `.dev.env`

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MODEL_REPO_ID` | string | `Qwen/Qwen2.5-Coder-3B-Instruct-GGUF` | HuggingFace repository ID |
| `MODEL_FILENAME` | string | `*q8_0.gguf` | Model file pattern (glob) |
| `MODEL_GPU_LAYERS` | int | `-1` | GPU layers (-1 = auto-detect) |
| `MODEL_CONTEXT_WINDOW` | int | `2048` | Max context tokens |
| `MODEL_MAX_TOKENS` | int | `64` (code) / `1024` (.dev.env) | Max response tokens |
| `CHAT_TEMPERATURE` | float | `0.7` | Response randomness (0.0-1.0) |
| `SYSTEM_MESSAGE` | string | "you are TACO Assistant..." | AI behavior definition |
| `USE_GPU` | bool | `false` | Enable GPU acceleration |

### Configuration Priority

1. Environment variables (highest priority)
2. `.env` file values
3. Default values in `Config` class (lowest priority)

### Model Selection Guide

The default model is `Qwen/Qwen2.5-Coder-3B-Instruct-GGUF`:
- **3B parameters**: Reasonable size for local inference
- **Instruct-tuned**: Optimized for following instructions
- **Coder variant**: Better at programming-related tasks
- **GGUF format**: Optimized for llama.cpp inference
- **q8_0 quantization**: Good balance of quality and size

**Alternative Models:**
- Smaller: `Qwen/Qwen2-0.5B-Instruct-GGUF` (~500MB)
- Larger: `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF` (~7GB)

---

## API Reference

### Endpoints

#### GET /

**Description:** Health check and welcome message.

**Response:**
```json
{
    "message": "Welcome to the TA Assistant API! check the api swagger at localhost:8899/docs"
}
```

#### POST /api/v1/chat

**Description:** Main chat endpoint for LLM interaction.

**Request:**
```json
{
    "prompt": "What is a list in Python?",
    "system_message": "You are a helpful Python tutor"  // optional
}
```

**Response:**
```json
{
    "response": "A list in Python is a mutable, ordered collection..."
}
```

**Error Response (500):**
```json
{
    "detail": "An error occurred while processing the chat request."
}
```

### Swagger Documentation

Available at runtime:
- **Swagger UI:** `http://localhost:8899/docs`
- **ReDoc:** `http://localhost:8899/redoc`
- **OpenAPI JSON:** `http://localhost:8899/openapi.json`

---

## Deployment Options

### Option 1: Local Development

```bash
# Install dependencies
poetry install

# Create .env from template
cp .dev.env .env

# Run with hot reload
poetry run uvicorn app.main:app --reload
# OR
make chat-api-service
```

**Access:** `http://localhost:8000`

### Option 2: Docker

```bash
# Build and run
docker compose up chat-service

# Background mode
docker compose up -d chat-service

# View logs
docker compose logs -f chat-service

# Stop
docker compose down
```

**Access:** `http://localhost:8899`

### Option 3: Docker with GPU (NVIDIA)

The current Dockerfile does not include GPU support. To enable:

1. Use NVIDIA CUDA base image
2. Install NVIDIA Container Toolkit on host
3. Add GPU configuration to docker-compose.yml:

```yaml
services:
  chat-service:
    # ... existing config ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## Development Workflow

### Adding a New Endpoint

1. **Create endpoint file** in `app/api/v1/`:
   ```python
   from fastapi import APIRouter
   router = APIRouter(tags=["New Feature"])

   @router.get("/new-endpoint")
   async def new_endpoint():
       return {"message": "Hello"}
   ```

2. **Register router** in `app/main.py`:
   ```python
   from app.api.v1.new_endpoints import router as new_router
   app.include_router(new_router, prefix="/api/v1")
   ```

### Adding a New Service

1. **Create service file** in `app/services/`:
   ```python
   from app.core.logger import logger
   from app.core.settings import get_settings

   config = get_settings()

   class NewService:
       def __init__(self):
           logger.info("Initializing NewService...")
   ```

2. **Import and use** in endpoint files.

### Adding New Configuration

1. Add variable to `Config` class in `settings.py`
2. Add documentation to `.dev.env`
3. Update environment-specific `.env` files

---

## Troubleshooting Guide

### Common Issues

#### Issue: Model download fails

**Symptoms:** Error during startup about HuggingFace download.

**Solutions:**
1. Check internet connectivity
2. Verify `MODEL_REPO_ID` is correct
3. Ensure sufficient disk space (~3GB for default model)
4. Try manual download: `huggingface-cli download <repo_id> <filename>`

#### Issue: Out of memory error

**Symptoms:** Application crashes during model loading or inference.

**Solutions:**
1. Use smaller model (e.g., `Qwen2-0.5B-Instruct`)
2. Reduce `MODEL_CONTEXT_WINDOW`
3. Reduce `MODEL_GPU_LAYERS` to offload fewer layers to GPU
4. Close other memory-intensive applications

#### Issue: Slow response times

**Symptoms:** API responses take many seconds.

**Solutions:**
1. Enable GPU acceleration (`USE_GPU=true`, proper `MODEL_GPU_LAYERS`)
2. Use smaller model
3. Reduce `MODEL_MAX_TOKENS`
4. Increase `MODEL_CONTEXT_WINDOW` (counterintuitively, can help with caching)

#### Issue: Docker container won't start

**Symptoms:** Container exits immediately.

**Solutions:**
1. Check logs: `docker compose logs chat-service`
2. Verify `.env` file exists and is properly configured
3. Ensure port 8899 is not in use
4. Check Docker has sufficient memory allocated

#### Issue: "Connection refused" when accessing API

**Symptoms:** Cannot reach API at expected URL.

**Solutions:**
1. Verify correct port (8000 for local, 8899 for Docker)
2. Check application is running
3. Ensure firewall allows connections
4. Use `127.0.0.1` instead of `localhost` if DNS issues

---

## Known Issues and Limitations

### Current Limitations

1. **Single-turn conversations only**
   - The API does not maintain conversation history
   - Each request is independent
   - The `Message` model in chat_endpoints.py is defined but unused

2. **No authentication/authorization**
   - API is open to all requests
   - No rate limiting
   - Not suitable for public deployment without additional security

3. **Synchronous LLM inference**
   - Model inference blocks the request handler
   - Long responses may cause timeout issues
   - No streaming response support

4. **No persistent storage**
   - No database integration
   - No conversation logging to disk
   - Session state not maintained

5. **Default token limits**
   - Code default is 64 tokens (very short)
   - `.dev.env` sets 1024, but code default may surprise developers
   - Inconsistency between code defaults and template

6. **GPU support limitations**
   - Docker image does not include CUDA
   - Requires manual configuration for GPU

### Code Quality Issues

1. **Discrepancy in `MODEL_MAX_TOKENS`**
   - `settings.py` default: 64
   - `.dev.env` template: 1024
   - Should be consistent

2. **Unused `Message` model**
   - Defined in chat_endpoints.py
   - Not used in current implementation
   - Suggests incomplete multi-turn conversation feature

3. **Limited error context**
   - Generic error message returned to clients
   - Stack traces only in logs
   - Could benefit from error codes

---

## Future Improvements

### Short-term Enhancements

1. **Streaming responses**
   - Implement Server-Sent Events (SSE)
   - Allow real-time token streaming
   - Improve perceived latency

2. **Conversation history**
   - Implement session management
   - Store message history
   - Enable multi-turn conversations

3. **Configuration validation**
   - Add Pydantic validation for Config class
   - Validate on startup
   - Fail fast with clear error messages

4. **Health check endpoint**
   - Add `/health` endpoint
   - Check model loaded status
   - Return memory usage statistics

### Medium-term Enhancements

1. **Authentication**
   - Add API key authentication
   - Implement rate limiting
   - Add user management

2. **Caching layer**
   - Cache common responses
   - Reduce LLM calls for repeated queries
   - Implement cache invalidation

3. **Metrics and monitoring**
   - Add Prometheus metrics
   - Track response times
   - Monitor model performance

4. **Testing suite**
   - Unit tests for services
   - Integration tests for endpoints
   - Load testing scripts

### Long-term Enhancements

1. **Multi-model support**
   - Allow switching between models
   - Support different models for different use cases
   - A/B testing capabilities

2. **Fine-tuning pipeline**
   - Tools for model fine-tuning
   - Domain-specific training
   - Feedback incorporation

3. **Horizontal scaling**
   - Load balancer support
   - Multiple worker instances
   - Distributed caching

---

## Appendix

### File Quick Reference

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI entry point |
| `app/api/v1/chat_endpoints.py` | Chat API definitions |
| `app/services/chat_service.py` | LLM interaction |
| `app/core/settings.py` | Configuration |
| `app/core/logger.py` | Logging setup |
| `pyproject.toml` | Poetry dependencies |
| `Dockerfile` | Container definition |
| `docker-compose.yml` | Service orchestration |
| `Makefile` | Development shortcuts |
| `.dev.env` | Environment template |
| `.gitignore` | Git ignore rules |

### Useful Commands

```bash
# Development
poetry install                          # Install dependencies
poetry run uvicorn app.main:app --reload # Run with reload
make clean                              # Clean cache files

# Docker
docker compose up chat-service          # Run container
docker compose down                     # Stop container
docker compose logs -f chat-service     # View logs
docker compose build                    # Rebuild image

# Testing
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'

# HuggingFace
huggingface-cli download <repo_id> <filename>  # Manual download
```

### Dependencies

From `pyproject.toml`:

| Package | Version | Purpose |
|---------|---------|---------|
| python | ^3.10 | Runtime |
| llama-cpp-python | ^0.3.5 | LLM inference |
| huggingface-hub | ^0.26.5 | Model downloads |
| python-dotenv | ^1.0.1 | Environment loading |
| fastapi | ^0.115.6 | Web framework |
| uvicorn | ^0.34.0 | ASGI server |
