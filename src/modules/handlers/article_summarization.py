from dataclasses import asdict

import pydantic
from groq import Groq
from langchain.output_parsers import PydanticOutputParser

from app import logger
from modules.models.llm import LanguageModelParams
from modules.models.article import ArticleAnalysisContentCreation
from modules.templates import SYSTEM_ARTICLE_ANALYSIS_TEMPLATE
from settings import GROQ_API_KEY


class ArticleSummarizationHandler:
    def __init__(self, llm_params: LanguageModelParams) -> None:
        article_model: PydanticOutputParser = PydanticOutputParser(pydantic_object=ArticleAnalysisContentCreation)
        self.system_message = SYSTEM_ARTICLE_ANALYSIS_TEMPLATE.format(
            format_instructions=article_model.get_format_instructions()
        )

        self.client = Groq(api_key=GROQ_API_KEY)
        self.llm_params = llm_params

    def __call__(self, article_content: str) -> ArticleAnalysisContentCreation:
        article_analytics_content: PydanticOutputParser = PydanticOutputParser(
            pydantic_object=ArticleAnalysisContentCreation
        )
        system_message = SYSTEM_ARTICLE_ANALYSIS_TEMPLATE.format(
            format_instructions=article_analytics_content.get_format_instructions()
        )

        logger.info(f"User => Start summarizing article content ...")
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
        try:
            result = completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during summarizing article content: {str(e)}")
            return f"Error during summarizing article content. {e}"

        try:
            analytics_content = ArticleAnalysisContentCreation.parse_raw(result)
        except pydantic.ValidationError as e:
            logger.error(f"Error during parsing article content: {str(e)}")
            return result

        return analytics_content
