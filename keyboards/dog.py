from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dog_menu_kb():
    kb_list = [
        [
            InlineKeyboardButton(text="🐶 Мои собачки и их задачи 📓", callback_data='my_dogs'),

        ],
        [
            InlineKeyboardButton(text="Добавить 🐶", callback_data='dog_add'),
            InlineKeyboardButton(text="Изменить 🐶", callback_data='dog_edit'),
            InlineKeyboardButton(text="Удалить 🐶", callback_data='todo_add'),


        ],
        [
            InlineKeyboardButton(text="Добавить 📓", callback_data='todo_add'),
            InlineKeyboardButton(text=" Удалить 📓", callback_data='todo_delete'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, one_time_keyboard=True)
    return keyboard

def only_add_dog_kb():
    kb_list = [
        [
            InlineKeyboardButton(text="Добавить собачку 🐶", callback_data='dog_add'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, one_time_keyboard=True)
    return keyboard