from config import *
import telebot
from telebot import types
from main import *

bot = telebot.TeleBot(token);

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    markup = types.ReplyKeyboardMarkup()
    buttonWrite = types.KeyboardButton('✍️  write password')
    buttonFind = types.KeyboardButton('🔍 find password')
    buttonUpdate = types.KeyboardButton('🔄 update password')

    markup.row(buttonWrite)
    markup.row(buttonFind)
    markup.row(buttonUpdate)

    if message.text == '✍️  write password':
        #write
        bot.send_message(message.from_user.id, "writing comming soon", reply_markup=markup)
    elif message.text == '🔍 find password':
        #find
        bot.send_message(message.from_user.id, "finding comming soon", reply_markup=markup)
    elif message.text == '🔄 update password':
        #update 
        bot.send_message(message.from_user.id, "updating comming soon", reply_markup=markup)
    else:
        pass

bot.polling(none_stop=True, interval=0)
