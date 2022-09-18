import telebot
from telebot import types
from config import *
from functions import *

bot = telebot.TeleBot(token)

# basic buttons for bot's work
basicMarkup = types.ReplyKeyboardMarkup()
button_write = types.KeyboardButton('✍️  write password')
button_find = types.KeyboardButton('🔍 find password')
button_update = types.KeyboardButton('🔄 update password')
button_settings = types.KeyboardButton("⚙️ change generator's settings")
button_random_password = types.KeyboardButton("❔ get password without saving")
# organizing of buttons
basicMarkup.row(button_find, button_write)
basicMarkup.row(button_update)
basicMarkup.row(button_settings)
basicMarkup.row(button_random_password)

# settings buttons
settingsMarkup = types.ReplyKeyboardMarkup()
button_uppercase = types.KeyboardButton('uppercase')
button_special_symbols = types.KeyboardButton('special symbols')
# organizing of buttons
settingsMarkup.row(button_uppercase)
settingsMarkup.row(button_special_symbols)


# functions
def add_user_to_database(message: telebot.types.Message) -> str:
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    try:
        cursor.execute("INSERT INTO users (id) VALUES (" + str(_id) + ");")
        connection.commit()
    except IndexError:
        print(f'user number {_id} already exists')


def get_settings(message: telebot.types.Message) -> [int, int]:
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    cursor.execute(f'SELECT specials, caps FROM users WHERE id = {_id};')
    special_symbols, uppercase = cursor.fetchone()
    return special_symbols, uppercase


def set_setting(setting: str, message: telebot.types.Message) -> str:
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    cursor.execute(f'UPDATE users SET {setting}= !{setting} WHERE id = {_id};')
    connection.commit()
    cursor.execute(f'SELECT {setting} FROM users WHERE id = {_id};')
    setting_value = cursor.fetchone()[0]
    print(setting_value)
    if (setting_value == 0):
        setting_value = "disabled"
    else:
        setting_value = "enabled"
    return f'your {setting} is {setting_value}'


def get_setting_to_update(message: telebot.types.Message):
    if message.text == "special symbols":
        result = set_setting("specials", message)
        bot.send_message(message.from_user.id, result, reply_markup=basicMarkup)
    elif message.text == "uppercase":
        result = set_setting("caps", message)
        bot.send_message(message.from_user.id, result, reply_markup=basicMarkup)
    else:
        bot.send_message(message.from_user.id, "please use th buttons next time", reply_markup=basicMarkup)


# main function

@bot.message_handler(content_types=["text"])
def main(message):
    if message.text == "/start":
        add_user_to_database(message)  # should create new user in database
        bot.send_message(message.from_user.id,
                         "Welcome.\n I am bnejor the bot who saves your passwords and generates safe passwords.\nthe "
                         "passwords are not are not crypted because of schema's settings but dont need to worry, "
                         "you anyway can change preset if you run the same bot on your own\nhave a nice experiense",
                         reply_markup=basicMarkup)

    elif message.text == "⚙️ change generator's settings":
        # change generate_password()'s Trues and Falses
        bot.send_message(message.from_user.id, "please use following buttons to change settings",
                         reply_markup=settingsMarkup)
        bot.register_next_step_handler(message, get_setting_to_update)

    elif message.text == "❔ get password without saving":
        # get settings
        special_symbols, uppercase = get_settings(message)
        bot.send_message(message.from_user.id, generate_password(special_symbols, uppercase), reply_markup=basicMarkup)

    else:
        bot.send_message(message.from_user.id, "please use the buttons", reply_markup=basicMarkup)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except IndexError:
        pass
