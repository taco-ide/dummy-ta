from os import environ
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

class Config:

    # HuggingFace Model Configurations
    MODEL_REPO_ID: str = environ.get("MODEL_REPO_ID", "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF")
    MODEL_FILENAME: str = environ.get("MODEL_FILENAME", "*q8_0.gguf")
    MODEL_GPU_LAYERS: int = int(environ.get("MODEL_GPU_LAYERS", -1)) # Use all available GPU layers.
    MODEL_CONTEXT_WINDOW: int = int(environ.get("MODEL_CONTEXT_WINDOW", 2048))  # Default context window size
    MODEL_MAX_TOKENS: int = int(environ.get("MODEL_MAX_TOKENS", 64))  # Default max tokens

    # Runtime Configurations
    USE_GPU: bool = environ.get("USE_GPU", "False").lower() == "true"  # Toggle GPU usage

def get_settings():
    return Config()

# Usage Example:
# from settings import get_settings
# config = get_settings()
# print(config.LOG_LEVEL)

