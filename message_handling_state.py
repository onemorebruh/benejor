from aiogram.filters.state import StatesGroup, State


class MessageHandlingState(StatesGroup):
    # shows default markup
    # after user action script is finished
    STATE_DEFAULT = State()

    # shows settings markup
    # is active after change settings button press
    STATE_SETTINGS = State()

    # doesn't need any markup
    # is active after find button press
    STATE_SEARCHING = State()