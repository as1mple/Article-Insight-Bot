from aiogram import Dispatcher, F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app import logger
from modules.handlers.scraping import HabrArticleParserHandler
from modules.handlers.article_summarization import ArticleSummarizationHandler
from settings import LLM_PARAMS

router = Router()

router.habr_handler = HabrArticleParserHandler()
router.article_summarization = ArticleSummarizationHandler(LLM_PARAMS)


class ArticleStates(StatesGroup):
    CHOOSING = State()
    SUMMARIZING = State()


@router.message((F.text == "Get today news 📰") | (F.text == "/today_news"))
async def cmd_get_today_news(message: Message, state: FSMContext):
    await message.answer("Getting today news 📰")
    logger.info(f"User [{message.chat.username}] => Getting today news ...")

    articles = router.habr_handler.get_top_articles().articles
    logger.info(f"User [{message.chat.username}] => Today news received. => {' | '.join([article.title for article in articles])}")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=article.title, callback_data=article.link)]
            for article in articles
        ]
    )

    await message.answer(
        text="Choose article:",
        reply_markup=buttons
    )
    await state.set_state(ArticleStates.CHOOSING)  # Переход в состояние выбора статьи


@router.callback_query(StateFilter("ArticleStates:CHOOSING"))
async def cmd_get_article_link(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    logger.info(f"User [{callback_query.message.chat.username}] => User choose article: {callback_query.data}")
    await callback_query.message.answer(
        f"‏‏‎ ‎\n ↻ <i>To read the article, follow the <a href='{callback_query.data}'>link</a></i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

    await state.update_data(article_link=callback_query.data)
    await state.set_state(ArticleStates.SUMMARIZING)

    bool_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Yes'), KeyboardButton(text='No')]],
        resize_keyboard=True,
    )
    await callback_query.message.answer(
        "Would you like to summarize the article text?", reply_markup=bool_keyboard
    )


@router.message(StateFilter("ArticleStates:SUMMARIZING"))
async def cmd_summarize_article(message: Message, state: FSMContext):
    # message.model_dump_json(indent=4, exclude_none=True)
    logger.info(f"User [{message.chat.username}] => User answer to summarize article: {message.text}")
    answer = message.text.lower()
    if answer == "yes":
        data = await state.get_data()
        article_link = data.get("article_link")

        await message.answer(f"Getting the article content...", reply_markup=ReplyKeyboardRemove())
        logger.info(f"User [{message.chat.username}] => Getting the article content ...")
        try:
            content = router.habr_handler.get_content(article_link)
        except IndexError as e:
            logger.error(f"User [{message.chat.username}] => Error during getting the article content: {str(e)}")
            await message.answer(f"Error during getting the article content")
            await state.set_state(ArticleStates.CHOOSING)

        else:
            logger.info(f"User [{message.chat.username}] => Article content received...")
            summarization_obj = router.article_summarization(content)

            await message.answer(str(summarization_obj))
    else:
        await message.answer("Ok, if you need a summary, feel free to ask!", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ArticleStates.CHOOSING)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_get_today_news)
    dp.register_callback_query_handler(cmd_get_article_link)
    dp.register_message_handler(cmd_summarize_article)
