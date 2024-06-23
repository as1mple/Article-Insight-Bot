import os

from modules.models.loger import LogHandler, Sink, LogLevel, LogConfig
from modules.models.llm import LanguageModelParams, LanguageModelVariants

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOKEN = os.getenv("TOKEN")

LLM_PARAMS = LanguageModelParams(
    model=LanguageModelVariants.Llama3_70b.value,
    temperature=0.5,
    max_tokens=4024,
    top_p=1,
    stream=False,
    stop=None
)

LOGGER_CONSOLE_CONFIG = LogHandler(
    sink=Sink.console.value,
    level=LogLevel.DEBUG.value,
    format="<green>{time}</green> {level} <level>{message}</level>",
    rotation=None
)

LOGGER_FILE_CONFIG = LogHandler(
    sink=Sink.file.value,
    level=LogLevel.INFO.value,
    format="{time} {level} {message}",
    rotation="1 weeks"
)

LOGCONFIG = LogConfig(handlers=[LOGGER_CONSOLE_CONFIG, LOGGER_FILE_CONFIG])
