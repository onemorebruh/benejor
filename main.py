import asyncio

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

import markups
from message_handling_state import MessageHandlingState
from config import *
from handlers.handler_commands import *
from handlers.handler_random_password import display_random_password
from handlers.handler_find_password import find_password
from handlers.handler_settings import *
from handlers.handler_write import *

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(storage=MemoryStorage())

password_description = dict()  # key is user_id value is valid description


@dp.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    await state.set_state(MessageHandlingState.STATE_DEFAULT)
    await init_user(message)
    return


@dp.message(MessageHandlingState.STATE_SEARCHING)
async def finding_password_handler(message: types.Message, state: FSMContext):
    await find_password(message, state)
    return


@dp.message(MessageHandlingState.STATE_WRITING_STEP1)
async def asking_for_description_handler(message: types.Message, state: FSMContext):
    await remember_description(message, state, password_description)

    await message.answer("Are you going to save already existing password or generate new one?",
                         reply_markup=markups.old_or_new_password_markup)
    return


@dp.message(MessageHandlingState.STATE_WRITING_STEP2)
async def finding_password_handler(message: types.Message, state: FSMContext):
    await route_new_or_old(message, state, password_description)
    return


@dp.message(MessageHandlingState.STATE_WRITING_STEP3)
async def finding_password_handler(message: types.Message, state: FSMContext):
    await write_existing_password(message, state, password_description)
    return


@dp.message()
async def message_router(message: types.Message, state: FSMContext) -> None:
    if message.text == "❔ get password without saving":
        await display_random_password(message)

    elif message.text == "🔍 find password":
        await state.set_state(MessageHandlingState.STATE_SEARCHING)
        await message.answer("Please, type password name")

    elif message.text == "✍️  write password":
        await message.answer("Please, write password's description")
        await state.set_state(MessageHandlingState.STATE_WRITING_STEP1)

    elif message.text == "⚙️ change generator's settings":
        await show_settings(message, state)

    else:
        await message.answer("The text you have just send it not a command. Please the button", reply_markup=default_markup)


@dp.callback_query()
async def setting_router(call: CallbackQuery):
    await change_setting(call)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot have been shut down")
