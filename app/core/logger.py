import logging

# Create a logger
logger = logging.getLogger("dummy_ta")
logger.setLevel(logging.DEBUG)  # Default to DEBUG for detailed logs

# Create a console handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # Default to DEBUG

# Define the logging format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
)
stream_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stream_handler)
