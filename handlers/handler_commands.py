from aiogram.types import Message

from config import *
from markups import *
from database_interaction import *


async def init_user(message: Message) -> None:
    # init new user
    _id = message.from_user.id
    try:
        db_execute_query(f"INSERT INTO user_settings (id) VALUES ({str(_id)});")
        db_execute_query(f"INSERT INTO user (id) VALUES ({str(_id)});")
    except:
        print(f'user number {_id} already exists')
    # send new user message
    await message.answer(
        text=f"""Welcome.
I am benejor. The bot who saves your passwords and generates safe passwords.
Your passwords would be saved on {OWNER_NAME}\'s machine.
Have a nice experience""",
        reply_markup=default_markup
    )
