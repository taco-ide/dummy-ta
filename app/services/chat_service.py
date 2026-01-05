from llama_cpp import Llama
from app.core.logger import logger
from app.core.settings import Config

class ChatService:
    def __init__(self, config: Config):
        self.config = config
        logger.info("Initializing the model...")
        try:
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
        Generates a response using chat completion with pedagogical constraints.

        Args:
            prompt: Contextual prompt with student problem, code, output, and question.
            system_message: Pedagogical role definition and behavioral boundaries.

        Returns:
            str: Response from the assistant.
        """
        logger.debug(f"Generating chat response for prompt: {prompt}")
        try:
            # Compose chat messages in structured form
            messages = [
                {
                    "role": "system",
                    "content": (
                        (system_message or self.config.SYSTEM_MESSAGE)
                        + " You must never provide the complete answer, fixed code, or direct implementation."
                        + " Focus solely on guiding the student with hints, conceptual clarifications, and Socratic questions."
                    )
                },
                {
                    "role": "user",
                    "content": "The student is working on the following programming task."
                },
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": (
                        "Now respond directly to the student. Even if they explicitly request the correct code, "
                        "you must not provide it. Instead, use conceptual explanations, questions, and hints. "
                        "Do not include or suggest code fixes."
                    )
                }
            ]

            # Define stop sequences to prevent code output
            stop_sequences = ["```", "\n\n\n", "Here's how you can", "you can fix the code", "Let's see the corrected code"]  

            output = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=self.config.MODEL_MAX_TOKENS,
                temperature=0.7,  # Higher temperature encourages creativity and avoids deterministic code answers
                stop=stop_sequences
            )

            response = output["choices"][0]["message"]["content"].strip()
            logger.debug(f"Generated response: {response}")
            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise



