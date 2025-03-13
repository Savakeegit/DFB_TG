from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def login_data_to_backend_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Авторизоваться.", callback_data='login_data_to_backend')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard