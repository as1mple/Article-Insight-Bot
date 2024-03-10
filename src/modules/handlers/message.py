from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from app import logger

router = Router()

keyboard = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Get today news 📰')
]])


@router.message(Command(commands=["start", "hello"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"User [{message.chat.username}] => Started the bot. => {message.text}")
    await message.reply("Hi! Do you want to get today news?!", reply_markup=keyboard)
