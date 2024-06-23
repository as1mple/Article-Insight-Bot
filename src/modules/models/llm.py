from dataclasses import dataclass
from enum import Enum


class LanguageModelVariants(Enum):
    Llama3_8b = "llama3-8b-8192"
    Llama3_70b = "llama3-70b"

    Mixtral_7b = "mixtral-8x7b-32768"
    Gemma_7b = "gemma-7b-it"


@dataclass
class LanguageModelParams:
    model: LanguageModelVariants
    temperature: float
    max_tokens: int
    top_p: int
    stream: bool
    stop: None | str
