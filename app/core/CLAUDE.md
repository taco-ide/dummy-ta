# CLAUDE.md - Core Module Context

## Overview

The `core/` directory contains cross-cutting concerns and utilities used throughout the application.

## Directory Structure

```
core/
├── __init__.py
├── logger.py            # Application logging configuration
└── settings.py          # Environment configuration management
```

## Components

### settings.py

Centralized configuration management using environment variables.

**Usage:**
```python
from app.core.settings import get_settings
config = get_settings()
print(config.MODEL_REPO_ID)
```

**Configuration Categories:**
1. **Model Settings**: HuggingFace repo, filename, GPU layers, context window, max tokens
2. **Chat Settings**: Temperature, system message
3. **Runtime Settings**: GPU usage toggle

**Environment Variables:**
| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_REPO_ID` | Qwen/Qwen2.5-Coder-3B-Instruct-GGUF | HuggingFace model repo |
| `MODEL_FILENAME` | *q8_0.gguf | Model file pattern |
| `MODEL_GPU_LAYERS` | -1 | GPU layers (-1 = auto) |
| `MODEL_CONTEXT_WINDOW` | 2048 | Context window size |
| `MODEL_MAX_TOKENS` | 64 | Max response tokens |
| `CHAT_TEMPERATURE` | 0.7 | Response randomness |
| `SYSTEM_MESSAGE` | "you are TACO Assistant..." | AI behavior prompt |
| `USE_GPU` | false | Enable GPU acceleration |

### logger.py

Pre-configured logging instance for consistent application logging.

**Usage:**
```python
from app.core.logger import logger

logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)  # Include stack trace
```

**Log Format:**
```
%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s
```

Example output:
```
2024-01-15 10:30:45,123 - INFO - dummy_ta - generate_response - Generating chat response
```

## Development Guidelines

### Adding New Settings

1. Add environment variable to `Config` class in `settings.py`
2. Provide sensible default values
3. Use appropriate type conversion (`int()`, `float()`, `.lower() == "true"`)
4. Document the variable in `.dev.env`
5. Update this CLAUDE.md with the new setting

### Logging Best Practices

- Use `logger.debug()` for detailed diagnostic info
- Use `logger.info()` for general operational events
- Use `logger.warning()` for recoverable issues
- Use `logger.error()` for failures (always with `exc_info=True` for exceptions)
- Never log sensitive data (API keys, passwords, etc.)

### Configuration Best Practices

- Always provide default values for non-critical settings
- Use environment variables for all deployment-specific values
- Keep `.env` out of version control (it's in `.gitignore`)
- Document all settings in `.dev.env` as a template
