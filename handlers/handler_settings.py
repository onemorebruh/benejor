from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from markups import *
from message_handling_state import *


async def show_settings(message: Message, state: FSMContext):
    # TODO get settings info

    # display info
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=settings_markup
    )
    await state.set_state(MessageHandlingState.STATE_SETTINGS)
