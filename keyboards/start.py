from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_login_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Войти", callback_data='login')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def start_registration_kb():
    kb_list = [
        [InlineKeyboardButton(text="❌Регистрация", callback_data='registration')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard