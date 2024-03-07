from dataclasses import asdict
from modules.handlers.article_summarization import LanguageModelParams, LanguageModelVariants, \
    ArticleSummarizationHandler

llm_params = LanguageModelParams(
    llm_model=LanguageModelVariants.Llama2_70b.value,
    temperature=0.5,
    max_tokens=4024,
    top_p=1,
    stream=False,
    stop=None
)

article_summarization = ArticleSummarizationHandler(asdict(llm_params))
