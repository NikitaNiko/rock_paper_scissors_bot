from aiogram import Router, F
from bot_start import bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot_keyboards.simple_keyboards import start_kb
from bot_data_base.bot_db import add_user, stop_search, finding, ret_find, playing_game
from bot_states.states import Form
from bot_keyboards.builder import build_kb

router = Router()

@router.message(F.text.lower() == "начать поиск")
async def rules(message: Message, state: FSMContext):
    await add_user(message.from_user.id, 1)
    await message.answer("Идет поиск...", reply_markup=build_kb('Отменить поиск'))
    await state.set_state(Form.one)
    await finding(message.from_user.id)


@router.message(Form.one, F.text.lower() == "🗿")
async def stop_finding(message: Message, state: FSMContext):
    f = await ret_find(message.from_user.id)
    if (f == 3):
        await playing_game(message.from_user.id, "камень")


@router.message(Form.one, F.text.lower() == "✂")
async def stop_finding(message: Message, state: FSMContext):
    f = await ret_find(message.from_user.id)
    if (f == 3):
        await playing_game(message.from_user.id, "ножницы")


@router.message(Form.one, F.text.lower() == "📃")
async def stop_finding(message: Message, state: FSMContext):
    f = await ret_find(message.from_user.id)
    if (f == 3):
        await playing_game(message.from_user.id, "бумага")


@router.message(Form.one, F.text.lower() == "завершить")
async def stop_finding(message: Message, state: FSMContext):
    f = await ret_find(message.from_user.id)
    if (f == 4):
        await message.answer("Ok!", reply_markup=start_kb)
        await state.clear()




@router.message(Form.one, F.text.lower() == "отменить поиск")
async def one(message: Message, state: FSMContext):
    f = await ret_find(message.from_user.id)
    if (f == 1):
        await stop_search(message.from_user.id)
        await message.answer("Поиск противника выключен", reply_markup=start_kb)
        await state.clear()


@router.message(Form.one)
async def one(message: Message, state: FSMContext):
    await message.answer("Если нужно отменить поиск - нажми на кнопку!", reply_markup=build_kb('Отменить поиск'))