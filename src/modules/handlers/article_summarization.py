from dataclasses import dataclass, asdict
from enum import Enum

from groq import Groq
from langchain.output_parsers import PydanticOutputParser

from modules.models.article import ArticleAnalysisContentCreation
from modules.templates import SYSTEM_INSTRUCTION_TEMPLATE
from modules.settings import GROQ_API_KEY


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


class ArticleSummarizationHandler:
    def __init__(self, llm_params: LanguageModelParams) -> None:
        article_model: PydanticOutputParser = PydanticOutputParser(pydantic_object=ArticleAnalysisContentCreation)
        self.system_message = SYSTEM_INSTRUCTION_TEMPLATE.format(
            format_instructions=article_model.get_format_instructions()
        )

        self.client = Groq(api_key=GROQ_API_KEY)
        self.llm_params = llm_params

    def __call__(self, article_content: str) -> ArticleAnalysisContentCreation:
        article_analytics_content: PydanticOutputParser = PydanticOutputParser(
            pydantic_object=ArticleAnalysisContentCreation
        )
        system_message = SYSTEM_INSTRUCTION_TEMPLATE.format(
            format_instructions=article_analytics_content.get_format_instructions()
        )

        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": f"<context>{article_content}</context>"
                },
            ],
            **asdict(self.llm_params)
        )

        result = completion.choices[0].message.content

        return ArticleAnalysisContentCreation.parse_raw(result)
