from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_kb():
    kb_list = [
        [
            InlineKeyboardButton(text="🐶 Управление собачками и их задачками 📓", callback_data='dogs_menu'),
        ],
        [
            InlineKeyboardButton(text="🌳 Точки выгула", callback_data='walks'),
            InlineKeyboardButton(text="🏥 Ветклиники", callback_data='vets')
        ],
        [
            InlineKeyboardButton(text="🧑‍🏫 Кинологи", callback_data='cynologists'),
            InlineKeyboardButton(text="🧠 Обучение", callback_data='lessons')
        ],
        [
            InlineKeyboardButton(text="🔎 Поиск собачек", callback_data='search'),
            InlineKeyboardButton(text="🚩 Статусы", callback_data='statuses')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, one_time_keyboard=True)
    return keyboard