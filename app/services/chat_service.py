from llama_cpp import Llama
from app.core.logger import logger
from app.core.settings import get_settings
from typing import List, Dict

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

    def generate_response(self, prompt: str, system_message: str = None) -> str:
        """
        Generates a response using chat completion for the given prompt.
        
        Args:
            prompt: The user's input message
            system_message: Optional system message to override default
        """
        logger.debug(f"Generating chat response for prompt: {prompt}")
        try:
            # Format the messages for chat completion
            messages = [
                {"role": "system", "content": system_message or config.SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ]
            
            # Use chat completion instead of text completion
            output = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=config.MODEL_MAX_TOKENS,
                temperature=config.CHAT_TEMPERATURE,  # Use configured temperature
                stop=None  # Let the model determine natural stopping points
            )
            
            # Extract the assistant's response from the chat completion
            response = output["choices"][0]["message"]["content"].strip()
            logger.debug(f"Generated response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise
