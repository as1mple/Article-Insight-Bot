from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str
    link: str


class DailyArticles(BaseModel):
    articles: list[Article]

    def __str__(self):
        articles_str = "\n".join([
            "\n".join([f"{field}: {getattr(article, field)}" for field in article.__fields__])
            for article in self.articles
        ])
        return f"DailyArticles:\n{articles_str}"


class ArticleAnalysisContentCreation(BaseModel):
    main_idea: str = Field(
        description="The core message or concept of the article, capturing the essence of what the article is about. " \
                    "Understanding the main idea is crucial for engaging content creation."
    )
    key_insights: str = Field(
        description="Important findings or observations extracted from the article. " \
                    "This includes summarizing significant points and their implications for a broader understanding."
    )
    benefits_of_reading: str = Field(
        description="What readers will gain by going through the article. " \
                    "This could relate to knowledge, insights, practical advice, or perspective enhancements."
    )
    target_audience: str = Field(
        description="Who will find the article most useful. This involves identifying the specific group or " \
                    "demographic that will benefit from the article's content the most."
    )
    engaging_post_format: str = Field(
        description="Guidelines for transforming the analysis into an interesting post that captivates the " \
                    "reader's attention and encourages engagement."
    )

    def __str__(self):
      return "\n".join([f"- {field.replace('_', ' ')}: {getattr(self, field)}"for field in list(self.__fields__)])
