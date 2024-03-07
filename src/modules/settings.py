import logging
import os


DEFAULT_DATA_RESOURCES_PATH: str = "resources/default_data_resources.json"

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

VERBOSE = 2

if VERBOSE == 0:
    LOGGING_LEVEL = logging.WARN
elif VERBOSE == 1:
    LOGGING_LEVEL = logging.INFO
elif VERBOSE == 2:
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO
