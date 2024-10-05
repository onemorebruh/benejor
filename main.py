import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message

import markups
from config import *
from handlers.handler_commands import *
from handlers.handler_random_password import display_random_password

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await init_user(message)
    return


@dp.message()
async def message_router(message: types.Message) -> None:
    if message.text == "❔ get password without saving":
        await display_random_password(message)
    else:
        await message.answer("the text you have just send it not a command. please the button")


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
