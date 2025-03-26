from os import listdir
from dotenv import dotenv_values

class Config:

    def __init__(self, filename: str):

        config = dotenv_values(filename)

        self.ASSISTANT_NAME: str = config["ASSISTANT_NAME"]
        self.ASSISTANT_DESCRIPTION: str = config["ASSISTANT_DESCRIPTION"]

        self.MODEL_REPO_ID: str = config["MODEL_REPO_ID"]
        self.MODEL_FILENAME: str = config.get("MODEL_FILENAME", "*.gguf")
        self.MODEL_GPU_LAYERS: int = int(config.get("MODEL_GPU_LAYERS", -1)) # Use all available GPU layers.
        self.MODEL_CONTEXT_WINDOW: int = int(config.get("MODEL_CONTEXT_WINDOW", 2048))  # Default context window size
        self.MODEL_MAX_TOKENS: int = int(config.get("MODEL_MAX_TOKENS", 64))  # Default max tokens

        # Chat Configurations
        self.CHAT_TEMPERATURE: float = float(config.get("CHAT_TEMPERATURE", 0.7))
        self.SYSTEM_MESSAGE: str = config.get(
            "SYSTEM_MESSAGE",
            "you are TACO Assistant, an dedicated AI assistant designed to help undergraduate students effectively learn Python programming."
        )

        # Runtime Configurations
        self.USE_GPU: bool = config.get("USE_GPU", "False").lower() == "true"  # Toggle GPU usage

def get_model_settings():
    """
    Retrieves a dictionary of all possible model settings in the 'models/'
    folder and returns the settings for the selected model.
    """
    models = {}
    for filename in listdir("models/"):
        if filename.endswith(".cfg"):
            model_name = filename.replace(".cfg", "")
            models[model_name] = Config(f"models/{filename}")
    return models
