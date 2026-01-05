# CLAUDE.md - Project Context for AI Assistants

## Project Overview

**dummy-ta** is a Teaching Assistant (TA) API implementation designed to help undergraduate students learn Python programming. It uses a local LLM powered by llama.cpp to provide intelligent chat-based assistance.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI with Uvicorn ASGI server
- **LLM Integration**: llama-cpp-python with Hugging Face Hub model downloads
- **Configuration**: python-dotenv for environment variable management
- **Dependency Management**: Poetry
- **Containerization**: Docker & Docker Compose

## Project Structure

```
.
├── app/                    # Main application code
│   ├── api/v1/            # API endpoints (versioned)
│   ├── core/              # Core configurations (settings, logging)
│   └── services/          # Business logic and LLM integration
├── docs/                   # Documentation assets
├── .vscode/               # VS Code debug configurations
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-service orchestration
├── Makefile               # Development shortcuts
└── pyproject.toml         # Poetry dependencies
```

## Development Commands

```bash
# Install dependencies
poetry install

# Run locally with hot reload
make chat-api-service
# OR
poetry run uvicorn app.main:app --reload

# Run with Docker
docker compose up chat-service

# Clean Python cache
make clean
```

## Environment Configuration

Copy `.dev.env` to `.env` and configure:

- `MODEL_REPO_ID`: HuggingFace model repository (default: Qwen2.5-Coder-3B-Instruct)
- `MODEL_FILENAME`: GGUF model file pattern
- `MODEL_GPU_LAYERS`: GPU layer offloading (-1 for auto)
- `MODEL_CONTEXT_WINDOW`: Context window size (default: 2048)
- `MODEL_MAX_TOKENS`: Max response tokens (default: 1024)
- `CHAT_TEMPERATURE`: Response randomness (0.0-1.0)
- `SYSTEM_MESSAGE`: AI behavior definition
- `USE_GPU`: Enable/disable GPU usage

## API Endpoints

- `GET /` - Health check / welcome message
- `POST /api/v1/chat` - Main chat endpoint
  - Request: `{"prompt": "string", "system_message": "optional string"}`
  - Response: `{"response": "string"}`

## API Documentation

Swagger UI available at: `http://localhost:8899/docs`

## Code Conventions

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Comprehensive error handling with proper logging
- Pydantic models for request/response validation
- Async/await pattern for FastAPI endpoints

## Key Files

- `app/main.py`: FastAPI application entry point with middleware and lifespan
- `app/api/v1/chat_endpoints.py`: Chat API endpoint definitions
- `app/services/chat_service.py`: LLM interaction logic
- `app/core/settings.py`: Configuration management
- `app/core/logger.py`: Logging setup

## Testing the API

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/chat' \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "what is a llm"}'
```

## Important Notes

1. The `.env` file contains sensitive configuration and is gitignored
2. First run will download the LLM model from HuggingFace (~3GB for default model)
3. GPU acceleration is optional but recommended for faster inference
4. Default port is 8899 (Docker) or 8000 (local development with --reload)
