import telebot
from telebot import types
from config import *
from functions import *

bot = telebot.TeleBot(token)


class UserRow:  # saves global information for each user
    description = ""

    def __init__(self, description):
        self.description = description


global_user_table = {}  # contains UserRows

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

# new or existing password buttons
passwordMarkup = types.ReplyKeyboardMarkup()
button_new = types.KeyboardButton("generate new password")
button_existed = types.KeyboardButton("write already existing password")
# organizing of buttons
passwordMarkup.row(button_new)
passwordMarkup.row(button_existed)


# functions
def add_user_to_database(message: telebot.types.Message):  # adds user for bot's work
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    try:
        cursor.execute("INSERT INTO user (id) VALUES (" + str(_id) + ");")
        connection.commit()
    except IndexError:
        print(f'user number {_id} already exists')


def get_settings(message: telebot.types.Message) -> [int, int]:  # get settings for password generating
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    cursor.execute(f'SELECT specials, caps FROM user WHERE id = {_id};')
    special_symbols, uppercase = cursor.fetchone()
    return special_symbols, uppercase


def set_setting(setting: str, message: telebot.types.Message) -> str:  # changes settings
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    cursor.execute(f'UPDATE user SET {setting}= !{setting} WHERE id = {_id};')
    connection.commit()
    cursor.execute(f'SELECT {setting} FROM user WHERE id = {_id};')
    setting_value = cursor.fetchone()[0]
    if setting_value == 0:
        setting_value = "disabled"
    else:
        setting_value = "enabled"
    return f'your {setting} is {setting_value}'


def get_setting_to_update(message: telebot.types.Message):  # gets info what setting have to be changed
    if message.text == "special symbols":
        result = set_setting("specials", message)
        bot.send_message(message.from_user.id, result, reply_markup=basicMarkup)
    elif message.text == "uppercase":
        result = set_setting("caps", message)
        bot.send_message(message.from_user.id, result, reply_markup=basicMarkup)
    else:
        bot.send_message(message.from_user.id, "please use th buttons next time", reply_markup=basicMarkup)


def ask_for_description(message: telebot.types.Message):  # writes description to global dictionary
    global global_user_table
    description = validate(message.text).lower()  # make description standardized
    global_user_table[message.from_user.id] = UserRow(description)
    bot.send_message(message.from_user.id, "are you going to generate new password or save already exiting one?",
                     reply_markup=passwordMarkup)
    bot.register_next_step_handler(message, write_password)


def write_existed_password(message: telebot.types.Message):  # writes password that bot don't need to generate
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    password = validate(message.text)
    cursor.execute(
        f'INSERT INTO password (user, password, description) VALUES ({_id}, "{encrypt(password, _id)}", "{global_user_table[_id].description}");')  # save password in database
    connection.commit()
    bot.send_message(message.from_user.id, f"password is {password}")
    bot.send_message(message.from_user.id, "password is successfully saved", reply_markup=basicMarkup)
    del global_user_table[_id]


def write_password(message: telebot.types.Message): # generates and writes password or delegates it to write_existed_password
    global global_user_table
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    if message.text == "write already existing password":
        # ask for password
        bot.send_message(message.from_user.id, "please write your password")
        bot.register_next_step_handler(message, write_existed_password)
    elif message.text == "generate new password":
        # generate password
        special_symbols, uppercase = get_settings(message)  # get settings
        password = generate_password(special_symbols, uppercase)  # generate password
        cursor.execute(
            f'INSERT INTO password (user, password, description) VALUES ({_id}, "{encrypt(password, _id)}", "{global_user_table[_id].description}");')  # save password in database
        connection.commit()
        bot.send_message(message.from_user.id, f"password is {password}")
        bot.send_message(message.from_user.id, "password is successfully saved", reply_markup=basicMarkup)
        del global_user_table[_id]

    else:
        bot.send_message(message.from_user.id, "please use th buttons next time", reply_markup=basicMarkup)
        del global_user_table[_id]


def find_password(message: telebot.types.Message):
    passwords = []
    descriptions = []
    description = message.text
    connection = connect(host, user, passwd, database)
    cursor = connection.cursor()
    _id = message.from_user.id
    cursor.execute(f"SELECT password, description FROM password WHERE user={_id} AND description LIKE '%{validate(description)}%'")
    result = cursor.fetchall()
    for each in result:
        passwords.append(each[0])
        if each[1] == "":
            descriptions.append("epmty string")
        else:
            descriptions.append(each[1])
    i = 0
    for i in range(len(passwords)):
        bot.send_message(message.from_user.id, f'password for {descriptions[i]} is {decrypt(passwords[i], _id)}')



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

    elif message.text == '✍️  write password':
        # write into database
        bot.send_message(message.from_user.id, "what the password will be used for?")
        bot.register_next_step_handler(message, ask_for_description)

    elif message.text == '🔍 find password':
        # find
        bot.send_message(message.from_user.id, "please enter something from description")
        bot.register_next_step_handler(message, find_password)

    elif message.text == "⚙️ change generator's settings":
        # change generate_password()'s Trues and Falses
        bot.send_message(message.from_user.id, "please use following buttons to change settings",
                         reply_markup=settingsMarkup)
        bot.register_next_step_handler(message, get_setting_to_update)

    elif message.text == "❔ get password without saving":
        # get settings
        special_symbols, uppercase = get_settings(message)
        # generate password
        bot.send_message(message.from_user.id, generate_password(special_symbols, uppercase), reply_markup=basicMarkup)

    else:
        bot.send_message(message.from_user.id, "please use the buttons", reply_markup=basicMarkup)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except IndexError:
        pass
