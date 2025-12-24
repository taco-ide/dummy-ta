# CLAUDE.md - Services Module Context

## Overview

The `services/` directory contains the business logic layer of the application, primarily handling LLM interactions.

## Directory Structure

```
services/
├── __init__.py
└── chat_service.py      # LLM chat interaction service
```

## Components

### ChatService (chat_service.py)

The main service class for interacting with the local LLM via llama-cpp-python.

**Responsibilities:**
- Initialize and manage the LLM model
- Format conversation messages
- Generate chat completions
- Handle LLM-specific errors

**Usage:**
```python
from app.services.chat_service import ChatService

chat_service = ChatService()
response = chat_service.generate_response(
    prompt="What is Python?",
    system_message="You are a helpful assistant"
)
```

## LLM Integration Details

### Model Loading
- Models are downloaded from HuggingFace Hub on first use
- Uses GGUF quantized format for efficient inference
- Supports GPU acceleration with configurable layer offloading

### Chat Completion Format
The service uses the chat completion API with the following message structure:
```python
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": prompt}
]
```

### Key Parameters
- `max_tokens`: Maximum tokens in the response
- `temperature`: Controls response randomness (0.0 = deterministic, 1.0 = creative)
- `stop`: Stop sequences (currently set to `None` for natural stopping)

## Development Guidelines

### Adding New Services

1. Create a new file in `services/` directory
2. Define a class with clear initialization and methods
3. Use `logger` for all logging
4. Load settings via `get_settings()`
5. Handle exceptions with proper logging

### Service Pattern Template

```python
from app.core.logger import logger
from app.core.settings import get_settings

config = get_settings()

class MyService:
    def __init__(self):
        logger.info("Initializing MyService...")
        try:
            # Initialization logic
            logger.info("MyService initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize MyService: {e}", exc_info=True)
            raise

    def my_method(self, param: str) -> str:
        """Method docstring explaining functionality."""
        logger.debug(f"Processing: {param}")
        try:
            # Business logic
            return result
        except Exception as e:
            logger.error(f"Error in my_method: {e}", exc_info=True)
            raise
```

### Error Handling

- Log all exceptions with `exc_info=True`
- Re-raise exceptions for the API layer to handle
- Don't catch exceptions silently
- Provide meaningful error messages for debugging

### Testing Services

Services can be tested independently:
```python
# Direct instantiation for testing
service = ChatService()
result = service.generate_response("test prompt")
```

## Performance Considerations

- The LLM model is loaded once during `ChatService` initialization
- Model loading takes significant time (first request may be slow)
- Consider connection pooling if adding database services
- Monitor memory usage with large context windows
