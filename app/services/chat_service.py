from llama_cpp import Llama
from app.core.logger import logger
from app.core.settings import get_settings

# Load settings
config = get_settings()

class ChatService:
    def __init__(self):
        logger.info("Initializing the model...")
        try:
            # Initialize the model
            self.llm = Llama.from_pretrained(
                repo_id=config.MODEL_REPO_ID,
                filename=config.MODEL_FILENAME,
                n_gpu_layers=config.MODEL_GPU_LAYERS,
                n_ctx=config.MODEL_CONTEXT_WINDOW,
            )
            logger.info("Model initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize the model: {str(e)}", exc_info=True)
            raise

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response for the given prompt using the model.
        """
        logger.debug(f"Generating response for prompt: {prompt}")
        try:
            output = self.llm(
                prompt,
                max_tokens=config.MODEL_MAX_TOKENS,  # Adjust token limit as needed
                stop=["Q:", "\n"],
                echo=False  # Only return the model's response
            )
            response = output["choices"][0]["text"].strip()
            logger.debug(f"Generated response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise
