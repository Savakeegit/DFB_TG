from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def registration_data_to_backend_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Зарегистрироваться", callback_data='registration_data_to_backend')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def to_login_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Авторизоваться", callback_data='login')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard