from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dog_menu_kb():
    kb_list = [
        [   InlineKeyboardButton(text="Подробно", callback_data='dogs_detail'),
            InlineKeyboardButton(text="Изменить данные", callback_data='dog_edit'),
            InlineKeyboardButton(text="Удалить", callback_data='dog_delete')
        ],
        [
            InlineKeyboardButton(text="Добавить собачку", callback_data='dog_add'),

        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list, one_time_keyboard=True)
    return keyboard