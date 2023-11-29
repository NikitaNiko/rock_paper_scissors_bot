from aiogram import Router, F
from aiogram.types import Message
from bot_keyboards.builder import build_kb


router = Router()

@router.message(F.text.lower() == "правила")
async def rules(message: Message):
    await message.answer("Игра длится 3 раунда.\n\nСуть игры заключается в слудующем:\n\
Вам предложено на выбор 3 предмета - это камень, ножницы и, соответственно, бумага.\n\
Камень ломает ножницы, ножницы режут бумагу, а бумага заворачивает в себя камень. \n\n\
Вам нужно выйграть 2 раунда для победы над противником, удачи!", reply_markup=build_kb('Начать поиск'))
    

