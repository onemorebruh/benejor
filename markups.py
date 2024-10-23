from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

default_markup = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🔍 find password"), types.KeyboardButton(text="✍️  write password")],
        [types.KeyboardButton(text="🔄 update password")],
        [types.KeyboardButton(text="⚙️ change generator's settings")],
        [types.KeyboardButton(text="❔ get password without saving")]
    ],
    resize_keyboard=True,
    input_field_placeholder="choose action by pressing button"
)

settings_markup = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="⬆️ uppercase")],
        [types.KeyboardButton(text="⁉ special symbols")]
    ],
    resize_keyboard=True,
    input_field_placeholder="change password generating settings"
)

old_or_new_password_markup = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="👶 generate new password")],
        [types.KeyboardButton(text="🧓 write already existing password")],
    ],
    resize_keyboard=True,
    input_field_placeholder="change password generating settings"
)


def inline_settings_markup(uppercase: bool, specials: bool):
    inline_kb_list = [
        [InlineKeyboardButton(text=f"uppercase is {uppercase}. click to set {not uppercase}", callback_data='UPPERCASE')],
        [InlineKeyboardButton(text=f"specials setting is {specials}. click to set {not specials}", callback_data='SPECIALS')],
        [InlineKeyboardButton(text=f"exit settings", callback_data='EXIT')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
