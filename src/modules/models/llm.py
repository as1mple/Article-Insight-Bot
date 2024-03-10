from dataclasses import dataclass
from enum import Enum


class LanguageModelVariants(Enum):
    Llama2_70b = "llama2-70b-4096"
    Mixtral_7b = "mixtral-8x7b-32768"


@dataclass
class LanguageModelParams:
    model: LanguageModelVariants
    temperature: float
    max_tokens: int
    top_p: int
    stream: bool
    stop: None | str
