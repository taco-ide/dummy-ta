
# dummy-ta

This is a dummy implementation of the TA API.

## Dependencies

The project uses the following Python libraries:

- `llama-cpp-python`: Local LLM inference via `llama.cpp`
- `huggingface-hub`: Load models from Hugging Face
- `fastapi`: Web API framework
- `uvicorn`: ASGI server
- `python-dotenv`: Environment variable loader
- `requests`: HTTP client used in test scripts (dev only)

## Requirements

- `Docker`: For containerized development and production environments.
- `Docker Compose`: To manage multi-container Docker applications. Currently only runs chat-service, but is prepared for future integration of additional services (like langfuse or databases).
- `Poetry`: For dependency management when running locally. Install it [here](https://python-poetry.org/docs/).

## How to Run

### Using Docker

```bash
# Build and run the Docker container:
docker compose up chat-service
```

### Running Locally

1. Install Poetry:
- Follow the installation instructions at Poetry's official site [here](https://python-poetry.org/docs/).

2. Install Dependencies:

```bash
poetry install
```

3. Run the Chat Service:

```bash
# using poetry directly
poetry run uvicorn app.main:app --reload

# Or using Makefile rule
make chat-api-service
```

## Testing the API

You can test the API in two ways:

### 1. Via `curl` Request

```bash
curl -X POST   http://127.0.0.1:8899/api/v1/chat   -H "accept: application/json"   -H "Content-Type: application/json"   -d '{
    "model": "knuth",
    "prompt": "Why is my code returning None?",
    "problem": "Write a function that returns the sum of two numbers.",
    "code": "def add(a, b):\n    result = a + b",
    "output": "None"
  }'
```

Expected response (example):

```json
{
  "response": "Let's think through this. You wrote a function that performs addition, but it is returning None. Could you check whether the function is using a `return` statement to output the result?"
}
```

### 2. Via Swagger UI

Access the interactive API docs at:

```
http://localhost:8899/docs
```

You will be able to test the `/chat` endpoint by providing:
- `model`
- `prompt`
- `problem`
- `code`
- `output`

Optional field:
- `system_message`

### 3. Running Guardrail Tests

```bash
# Run full suite of tests
poetry run python Test/test_guardrails.py --input Test/test_cases.json
```

#### Guardrail Testing

The script `Test/test_guardrails.py` tests whether the LLM respects the pedagogical policy (no direct answers). It evaluates answers against known correct outputs (`correct_solution`) and logs results with:

- PASS: Model avoided solution
- FAIL: Model included direct solution

Logs are saved in `Test/logs/guardrail_test_log_<timestamp>.json`

## Project Structure

```bash

dummy-ta/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── chat_endpoints.py       # FastAPI routes
│   ├── core/
│   │   ├── logger.py                   # Logger setup
│   │   └── settings.py                 # Config parsing
│   ├── services/
│   │   ├── chat_service.py             # LLM prompt orchestration
│   │   └── main.py                     # FastAPI app
├── docs/
├── models/                             # Model config files
│   ├── knuth.cfg
│   └── quentin.cfg
├── Test/
│   ├── test_cases.json                 # Full test suite
│   └── test_guardrails.py              # Test runner script
│   └─── logs/                          # Guardrail test logs
│        └── guardrail_test_log_*.json
├── .env
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── poetry.lock
├── README.md
```
