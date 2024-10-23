from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from markups import *
from usersetting import UserSetting
from message_handling_state import *
from database_interaction import *


async def show_settings(message: Message, state: FSMContext):
    await state.set_state(MessageHandlingState.STATE_SETTINGS)
    uppercase, specials = db_get_user_settings(str(message.from_user.id))

    await message.answer(
        text="current settings:",
        reply_markup=inline_settings_markup(uppercase, specials)
    )


async def change_setting(call: CallbackQuery):
    if call.data == "UPPERCASE":
        # update setting
        db_change_user_setting(call.from_user.id, UserSetting.UPPERCASE)
        # update inline markup
        uppercase, specials = db_get_user_settings(str(call.from_user.id))
        await call.message.edit_reply_markup(reply_markup=inline_settings_markup(uppercase, specials))
    elif call.data == "SPECIALS":
        # update setting
        db_change_user_setting(call.from_user.id, UserSetting.SPECIALS)
        # update inline markup
        uppercase, specials = db_get_user_settings(str(call.from_user.id))
        await call.message.edit_reply_markup(reply_markup=inline_settings_markup(uppercase, specials))
    elif call.data == "EXIT":
        await call.message.delete_reply_markup()
    else:
        await call.answer("unexpected data", show_alert=True)
