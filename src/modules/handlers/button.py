from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from modules.handlers.scraping import HabrArticleParserHandler

router = Router()


@router.message((F.text == "Get today news 📰") | (F.text == "/today_news"))
async def cmd_get_today_news(message: Message):
    await message.answer("Getting today news 📰")
    habr_handler = HabrArticleParserHandler()
    articles = habr_handler.get_top_articles().articles
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


@router.callback_query()
async def cmd_get_article_link(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        f"‏‏‎ ‎\n ↻ <i>To read the article, follow the <a href='{callback_query.data}'>link</a></i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
