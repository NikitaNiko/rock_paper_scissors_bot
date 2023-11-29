from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="Начать поиск"),
        ],
        [
            KeyboardButton(text="Правила"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="КАМЕНЬ! НОЖНИЦЫ! БУМАГА!"
)