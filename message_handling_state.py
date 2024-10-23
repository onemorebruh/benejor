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

    # shows old_or_new_markup
    # is active when user have to choose are they going to generate password or write existing one
    STATE_WRITING_STEP1 = State()

    # doesn't need any markup
    # is active when user have to type description of password
    STATE_WRITING_STEP2 = State()

    # doesn't need any markup
    # is active when user writes already existing password
    STATE_WRITING_STEP3 = State()
