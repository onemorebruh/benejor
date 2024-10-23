from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from message_handling_state import MessageHandlingState
from database_interaction import db_find_passwords_by_name
from pass_gen_lib import make_valid


async def find_password(message: Message, state: FSMContext):
    passwords = db_find_passwords_by_name(message.text, message.from_user.id)

    # display each password
    for key in passwords.keys():
        await message.answer(text=f"password for <b>{key}</b> is <code>{passwords[key]}</code>",
                             parse_mode=ParseMode.HTML)

    # lose state
    await state.set_state(MessageHandlingState.STATE_DEFAULT)
    return
