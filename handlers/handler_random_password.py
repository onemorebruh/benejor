from aiogram.types import Message

from pass_gen_lib import *
from markups import *
from database_interaction import *

async def display_random_password(message: Message):
    uppercase, specials = db_get_user_settings(message.from_user.id)
    password = generate_password(specials, uppercase)
    await message.answer(
        text=f"""{password}""",
        reply_markup=default_markup
    )