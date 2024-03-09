from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

router = Router()

keyboard = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Get today news 📰')
]])


@router.message(Command(commands=["start", "hello"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    await message.reply("Hi!", reply_markup=keyboard)
