from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_kb(my_buttons: str|list, buttons_in_line=1):
    items = my_buttons

    if (isinstance(items, str)):
        items = [items]

    builder = ReplyKeyboardBuilder()
    [builder.button(text = item) for item in items]

    builder.adjust=buttons_in_line

    return builder.as_markup(resize_keyboard=True)