from os import stat
from config import *
import telebot
from telebot import types
from main import *

bot = telebot.TeleBot(token);

class user_row():# for global_user_table only
    spec = ""
    caps = ""
    id = 0
    description = ""
    password = ""

    def __init__(self, spec, caps, id, description):
        self.spec = spec
        self.caps = caps
        self.id = id
        self.description = description
        self.password = generate_password(spec, caps, id)

class status_bar():
    def __init__(self, spec, up):
        self.spec = spec
        self.up = up

global_user_table = {}# helps in using functions
global_statuses = {}# like user_table but simpler

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    try:
        spec_status = global_statuses[str(message.from_user.id)].spec
        up_status = global_statuses[str(message.from_user.id)].up
    except:
        spec_status = "special symbols"
        up_status = "upper words"
     # basic markup
    
    markup = types.ReplyKeyboardMarkup()
    buttonWrite = types.KeyboardButton('✍️  write password')
    buttonFind = types.KeyboardButton('🔍 find password')
    buttonUpdate = types.KeyboardButton('🔄 update password')
    buttonSettings = types.KeyboardButton("⚙️ change generator's settings") # TODO build abbility to change
    buttonRandomPassword = types.KeyboardButton("❔ get password without saving")
    
    markup.row(buttonWrite)
    markup.row(buttonFind)
    markup.row(buttonUpdate)
    markup.row(buttonSettings)
    markup.row(buttonRandomPassword)

    # comfiguration markup
    conf = types.ReplyKeyboardMarkup()
    specials = types.KeyboardButton(spec_status)# TODO add t/f emojis
    caps =types.KeyboardButton(up_status)

    conf.row(specials)
    conf.row(caps)

    #the main code starts here
    if message.text == '✍️  write password':
        #write
        bot.send_message(message.from_user.id, "what the password will be used for?")
        bot.register_next_step_handler(message, ask_description)
    elif message.text == '🔍 find password':
        #find
        bot.send_message(message.from_user.id, "please enter something from description")
        bot.register_next_step_handler(message, find_password_step_one)
    elif message.text == '🔄 update password':
        #update 
        bot.send_message(message.from_user.id, "plesase enter something from description")
        bot.register_next_step_handler(message, updete_step_one)
    elif message.text == "⚙️ change generator's settings":
        # change generate_password()'s Trues and Falses
        bot.send_message(message.from_user.id, "please use following buttons to change settings", reply_markup=conf)
        bot.register_next_step_handler(message, set_settings)
    elif message.text == "❔ get password without saving":
        bot.send_message(message.from_user.id, generate_password(True, True, message.from_user.id), reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, "please use the buttons", reply_markup=markup)
def find_password_step_one(message):
    connection = connect(host, user, passwd, database)
    description = message.text
    if description == "'":
        description = ""
    list_of_passwords = find(validate(description), message.from_user.id, connection)
    # format list to good looking string
    list_of_passwords = str(list_of_passwords).replace(", ", "\n").replace("('", "").replace("[", "").replace("',)", "").replace("]", "")
    bot.send_message(message.from_user.id, list_of_passwords)
def write_password_step_one(message):

    # write markup
    old_or_new = types.ReplyKeyboardMarkup()
    buttonOld = types.KeyboardButton("write alreadey existing password")
    buttonNew = types.KeyboardButton("generate new password")

    old_or_new.row(buttonOld)
    old_or_new.row(buttonNew)

    if message.text == "write alreadey existing password":
        bot.send_message(message.from_user.id, "type the password")
        bot.register_next_step_handler(message, ask_password)
    elif message.text == "generate new password":
        bot.send_message(message.from_user.id, "just write something, and i will send you password back")
        bot.register_next_step_handler(message,writing_final)
    else:
        bot.send_message(message.from_user.id, "please use the buttons", reply_markup=old_or_new)


def ask_description(message):
    # write markup
    old_or_new = types.ReplyKeyboardMarkup()
    buttonOld = types.KeyboardButton("write alreadey existing password")
    buttonNew = types.KeyboardButton("generate new password")

    old_or_new.row(buttonOld)
    old_or_new.row(buttonNew)

    global global_user_table
    bot.send_message(message.from_user.id, "are you goung to generate new password or save already exiting one?", reply_markup=old_or_new)
    connection = connect(host, user, passwd, database)
    spec, up = get_settings(message.from_user.id, connection)
    global_user_table[str(message.from_user.id)] = user_row(spec, up, message.from_user.id, message.text)
    bot.register_next_step_handler(message, write_password_step_one)

def writing_final(message):
    global global_user_table
    connection = connect(host, user, passwd, database)
    status = write(validate(global_user_table[str(message.from_user.id)].password), validate(global_user_table[str(message.from_user.id)].description), message.from_user.id, connection)
    bot.send_message(message.from_user.id, "your new password is saved\n" + validate(str(global_user_table[str(message.from_user.id)].password)))
    del global_user_table[str(message.from_user.id)]

def ask_password(message):
    # for old passwords only
    global global_user_table
    global_user_table[str(message.from_user.id)].password = message.text
    bot.send_message(message.from_user.id, "just write something, and i will send you password back")
    bot.register_next_step_handler(message, writing_final)

def updete_step_one(message):
    description = message.text
    connection = connect(host, user, passwd, database)
    password = generate_password(True, True, message.from_user.id)
    update_password(password, description, message.from_user.id, connection)
    bot.send_message(message.from_user.id, "password for " + validate(str(description)) + " is now\n" + str(password))

def set_settings(message):
    global global_statuses
    connection = connect(host,user, passwd, database)
    spec, up = get_settings(message.from_user.id, connection)
    if message.text == "special symbols":
        if spec == True:
            status = set_setting(message.from_user.id, connection, "specials", "F")
        else:
            status = set_setting(message.from_user.id, connection, "specials", "T")
    elif message.text == "upper words":
        if up == True:
            status = set_setting(message.from_user.id, connection, "caps", "F")
        else:
            status = set_setting(message.from_user.id, connection, "caps", "T")
    bot.send_message(message.from_user.id, status)




bot.polling(none_stop=True, interval=0)
