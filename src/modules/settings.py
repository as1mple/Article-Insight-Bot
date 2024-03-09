import logging
import os

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
TOKEN = os.getenv("TOKEN")

VERBOSE = 2

if VERBOSE == 0:
    LOGGING_LEVEL = logging.WARN
elif VERBOSE == 1:
    LOGGING_LEVEL = logging.INFO
elif VERBOSE == 2:
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO
