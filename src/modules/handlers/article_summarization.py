from dataclasses import dataclass, asdict
from enum import Enum

from groq import Groq
from langchain.output_parsers import PydanticOutputParser

from modules.models.link_parser import ArticleSummarize, ArticleAnalysisContentCreation
from modules.templates import SYSTEM_INSTRUCTION_TEMPLATE
from modules.handlers.parser import ContentParserHandler
from modules.settings import GROQ_API_KEY


class LanguageModelVariants(Enum):
    Llama2_70b = "Llama2-70b-4096"
    Mixtral_7b = "mixtral-8x7b-32768"


@dataclass
class LanguageModelParams:
    llm_model: LanguageModelVariants
    temperature: float
    max_tokens: int
    top_p: int
    stream: bool
    stop: None | str


class ArticleSummarizationHandler:
    def __init__(self, llm_params: LanguageModelParams) -> None:
        self.scraper = ContentParserHandler()

        article_model: PydanticOutputParser = PydanticOutputParser(pydantic_object=ArticleAnalysisContentCreation)
        self.system_message = SYSTEM_INSTRUCTION_TEMPLATE.format(
            format_instructions=article_model.get_format_instructions()
        )

        self.client = Groq(api_key=GROQ_API_KEY)
        self.llm_params = llm_params

        # self.logger = BaseLogger(__name__)

    def __call__(self, url: str, path_to_save: str) -> ArticleSummarize:
        article_content = self.scraper.parse_url(url)
        # self.scraper.save_to_file(article_content, path_to_save)

        article_analytics_content: PydanticOutputParser = PydanticOutputParser(
            pydantic_object=ArticleAnalysisContentCreation
        )
        system_message = SYSTEM_INSTRUCTION_TEMPLATE.format(
            format_instructions=article_analytics_content.get_format_instructions()
        )

        completion = self.client.messages.create(
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
