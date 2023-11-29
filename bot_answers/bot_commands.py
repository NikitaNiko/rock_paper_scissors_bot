from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from bot_keyboards.simple_keyboards import start_kb


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! \
\nЯ - бот для игры в камень ножницы бумага. Нажимай \"Начать поиск\" для подбора противника \
или можешь посмотреть правила игры, отправив мне сообщение \"Правила\"", reply_markup=start_kb)