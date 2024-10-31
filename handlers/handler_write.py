from aiogram import types
from aiogram.fsm.context import FSMContext
from message_handling_state import MessageHandlingState
from aiogram.enums import ParseMode

from pass_gen_lib import make_valid, generate_password
from message_handling_state import MessageHandlingState
from database_interaction import db_get_user_settings, db_write_password

from markups import default_markup


async def remember_description(message: types.Message, state: FSMContext, password_description: dict):
    password_description[message.from_user.id] = make_valid(message.text)
    await state.set_state(MessageHandlingState.STATE_WRITING_STEP2)


async def route_new_or_old(message: types.Message, state: FSMContext, password_description: dict):
    if message.text == "👶 generate new password":
        # if password is new user don't need to type value, so it generates instantly
        uppercase, specials = db_get_user_settings(message.from_user.id)
        password = generate_password(specials, uppercase)

        description = password_description[message.from_user.id]

        # write password to database
        db_write_password(message.from_user.id, description, password)

        # reset state
        await state.set_state(MessageHandlingState.STATE_DEFAULT)

        await message.answer(f"the password for <b>{description}</b> is <code>{password}</code>",
                             parse_mode=ParseMode.HTML,
                             reply_markup=default_markup)

    elif message.text == "🧓 write already existing password":
        await state.set_state(MessageHandlingState.STATE_WRITING_STEP3)

        await message.answer("Write existing password")
    else:
        pass


async def write_existing_password(message: types.Message, state: FSMContext, password_description: dict):
    # init variables
    description = password_description[message.from_user.id]
    password = message.text

    # write password to database
    db_write_password(message.from_user.id, description, password)

    # reset state
    await state.set_state(MessageHandlingState.STATE_DEFAULT)

    await message.answer(f"the password for <b>{description}</b> is <code>{password}</code>",
                         parse_mode=ParseMode.HTML,
                         reply_markup=default_markup)
