#  ____    _____   __   __   _____   _____   _____   ____
# |####\  |#####| |##\ |##| |#####| |#####| /#####\ |####\
# |#|_|#| |#|‾‾‾  |###\|##| |#|‾‾‾   ‾|#|‾  |#|‾|#| |#|_|#|
# |####<  |#####| |##\# ##| |#####| _ |#|   |#| |#| |####<
# |#|_|#\ |#|‾‾‾  |##|\###| |#|‾‾‾ |#\/#|   |#|_|#| |#|‾\#\
# |#####/ |#####| |##| |##| |#####| \##/    \#####/ |#| |#|
#  ‾‾‾‾‾   ‾‾‾‾‾   ‾‾   ‾‾   ‾‾‾‾‾   ‾‾      ‾‾‾‾    ‾   ‾

import random
import mysql.connector
from mysql.connector import Error
import datetime

def connect():
    connection = None
    try:
        connection = mysql.connector.connect( 
            host="127.0.0.1",
            user="tgBot",
            passwd="L3t M3 1n!",
            database="password_bot"
        )
        print("mysql connected")
    except Error as e:
        print(f"'{e}'")
    return connection

def charge(list_of_elements, maximum):
    number = 0
    string = ''.join(list_of_elements)
    the_biggets_element = {"index": 0, "len": 0} #index
    while len(string) < maximum:
        # add new word
        dictionary = open("./dictionary.txt").read()
        dictionary = dictionary.split('\n')
        number = random.randint(0, len(dictionary))
        list_of_elements.append(dictionary[number])
        #clear the string form old data to plug new data into it
        string = ''
        string = ''.join(list_of_elements)
    number = 0
    if len(string) > maximum: # database is ready for passwords which are smaller then 51 symbol so it deletes the biggest element
        for each in list_of_elements:
            if len(each) > the_biggets_element["len"]:
                the_biggets_element['len'] = len(each)
                the_biggets_element['index'] = number
            number += 1
        list_of_elements.pop(the_biggets_element['index'])# works correctly
    return list_of_elements #sucess 

def generate_password(special_symbols, prefered_words, CAPS, crypting_key):
    # special_symbols - t/f allow it or not
    # prefered words - t/f ask user about the words it wants in password
    # CAPS - t/f should password contain upper and downer letters
    # crypting_key - string - crypts the generated password before plugining it into bd and helps to encrypt
    specials = ["#", "*", "(", ")", "$", "@", "!", "%", "?"]# TODO add more
    password_list = [] #it will contain all the symbols
    password = ''
    number = 0 #just for a few tasks
    words = "" #for adding prefered words
    if special_symbols == True:
        number = random.randint(0, int(len(specials) - 1))
        password_list.append(specials[number])
    if prefered_words == True:
        words = input("write the words you wnat in your password(50 letters max)")
        words.split(" ", ", ")# TODO plug new words in to dictionaty.txt
    # cycle plugs words into password list untils it have 50 symbols
    password_list = charge(password_list, 50)
    #TODO make random letters Upppder
    random.shuffle(password_list)# mistake is here
    password = ''.join(password_list)
    return password

id = 491770917
date = str(datetime.datetime.today()).split()[0]

#password = generate_password(True, False, False, str(id))

# CLI prototype
# start
# telegram user prints "/start" and bot check does such user exisit
while True:
    connection = connect()
    cursor = connection.cursor()
    print("what you need? \n[find] - find password by description\n[write] - write new password into database\n[update password] - update already existed password")
    action = input(":")
    if action == "[find]":
        description = input("type description") # TODO make search by description
        cursor.execute("SELECT password FROM user" + str(id) + " WHERE description LIKE'%" + description + "%';")
        print(cursor.fetchall())
    elif action == "[write]":
        print("do you want to save old password or generate new one?")
        print("[save old]\n[generate new]")
        new_or_old = input(":")
        if new_or_old == "[save old]":
            password = input("type the password you want to save")
        elif new_or_old == "[generate new]":
            # TODO ask for spesial symbols prefered words and caps
            password = generate_password(True, False, False, str(id))
            print('your password is ' + password)
        else:
            print("something is wrong. :( please try push one of the buttons")
        description = input("type description for your password, for example [facebook.com]")
        # sql request
        try:
            cursor.execute("INSERT INTO user" + str(id) + " (date, password, description) VALUES ('" + str(date) + "', '" + str(password) + "', '" + str(description) + "');")
            connection.commit()
        except:# there is no table for this user so create it
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE user" + str(id) + " ( \
                id int AUTO_INCREMENT NOT NULL, \
                date date NOT NULL, \
                password varchar(50) NOT NULL, \
                description varchar(255) DEFAULT NULL, \
                PRIMARY KEY (id);")
            connection.commit()
            cursor.execute("INSERT INTO users VALUES (" + str(id) + ");")
            connection.commit()
            #insert data again
            cursor.execute("INSERT INTO user" + str(id) + " (date, password, description) VALUES ('" + str(date) + "', '" + str(password) + "', '" + str(description) + "');")
            connection.commit()
    elif action == "[update password]": #update old password
        password = generate_password(True, False, False, str(id))
        description = input("write something from description")
        try:
            cursor.execute("UPDATE user" + str(id) + " SET password = '" + password + "', date = '" + date + "' WHERE description LIKE '%" + description + "%';")
            connection.commit()
        except:
            print("something is wrong with your description")
    else:
        print("please tap the button, do not send text")

