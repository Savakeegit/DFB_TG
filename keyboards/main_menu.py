from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def to_main_menu_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Перейти в главное меню", callback_data='main_menu')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, one_time_keyboard=True)
    return keyboard

def main_menu_kb():
    kb_list = [
        [
            InlineKeyboardButton(text="Мои собачки", callback_data='dogs'),
            InlineKeyboardButton(text="Поиск собачек", callback_data='dogs_search')
        ],
        [
            InlineKeyboardButton(text="Список ветклиник", callback_data='vet_list'),
            InlineKeyboardButton(text="Список точек выгула", callback_data='walk_list')
        ],
        [
            InlineKeyboardButton(text="Руководства", callback_data='guides'),
            InlineKeyboardButton(text="Личный кабинет", callback_data='user_account')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, one_time_keyboard=True)
    return keyboard