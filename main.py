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
from config import *

def connect(host, user, passwd, database):
    connection = None
    try:
        connection = mysql.connector.connect( 
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        print("mysql connected")
    except Error as e:
        print(f"'{e}'")
    return connection

def write(password, description, id, connection):
    cursor = connection.cursor()
    date = str(datetime.datetime.today()).split()[0]
    # sql request
    try:
        cursor.execute("INSERT INTO user" + str(id) + " (date, password, description) VALUES ('" + str(date) + "', '" + str(password) + "', '" + str(description) + "');")
        connection.commit()
    except:# there is no table for this user so create it
        cursor.execute("CREATE TABLE user" + str(id) + " (id int AUTO_INCREMENT NOT NULL, date date NOT NULL, password varchar(50) NOT NULL, description varchar(255) DEFAULT NULL, PRIMARY KEY (id));")
        connection.commit()
        cursor.execute("INSERT INTO users (id) VALUES (" + str(id) + ");")
        connection.commit()
        #insert data again
        cursor.execute("INSERT INTO user" + str(id) + " (date, password, description) VALUES ('" + str(date) + "', '" + str(password) + "', '" + str(description) + "');")
        connection.commit()
    return "succes"

def find(description, id, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM user" + str(id) + " WHERE description LIKE'%" + description + "%';")
    return cursor.fetchall()

def update_password(password, description, id, connection):
    cursor = connection.cursor()
    date = str(datetime.datetime.today()).split()[0]
    try:
        cursor.execute("UPDATE user" + str(id) + " SET password = '" + password + "', date = '" + date + "' WHERE description LIKE '%" + description + "%';")
        connection.commit()
        return "succes"
    except Error as e:
        print(f'{e}')
        return "something is wrong with your description"

def charge(list_of_elements, maximum):
    number = 0
    string = ''.join(list_of_elements)
    upper = True # contains data about randomly chosen action, so true makes 1 word upper
    the_biggets_element = {"index": 0, "len": 0}
    while len(string) < maximum:
        # add new word
        dictionary = open("./dependencies/dictionary.txt").read()
        dictionary = dictionary.split('\n')
        number = random.randint(0, int(len(dictionary)-1))
        # makes the word randomly Upper
        upper = random.choice([True, False])
        if upper == True:
            list_of_elements.append(dictionary[number].upper())
        else:
            list_of_elements.append(dictionary[number])
        #check element for being the biggest so programm can fastly delete it if the massive is too big
        if len(dictionary[number]) > the_biggets_element["len"]:
            the_biggets_element['len'] = len(dictionary[number])
            the_biggets_element['index'] = int(len(list_of_elements) - 1)
        #clear the string form old data to plug new data into it
        string = ''
        string = ''.join(list_of_elements)
    number = 0
    if len(string) > maximum: # database is ready for passwords which are smaller then 51 symbol so it deletes the biggest element
        try:
            list_of_elements.pop(the_biggets_element['index'])# works correctly
        except:
            while len(string) > maximum:
                list_of_elements.pop()
                sring = ''
                string = ''.join(list_of_elements)
    return list_of_elements #sucess 

def generate_password(special_symbols, CAPS, crypting_key):
    # special_symbols - t/f allow it or not
    # prefered words - t/f ask user about the words it wants in password
    # CAPS - t/f should password contain upper and downer letters
    # crypting_key - string - crypts the generated password before plugining it into bd and helps to encrypt
    specials = ["!",  "#",  "$", "%", "&", "(", ")", "*" "+", ",", "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "<", "=", ">", "?", "_", "@", "[", "]", "{", "}"]
    password_list = [] #it will contain all the symbols
    password = ''
    number = 0 #just for a few tasks
    words = "" #for adding prefered words
    if special_symbols == True:
        number = random.randint(0, int(len(specials) - 1))
        password_list.append(specials[number]) 
    # cycle plugs words into password list untils it have 50 symbols
    password_list = charge(password_list, 50)
    random.shuffle(password_list)# mistake is here
    password = ''.join(password_list)
    print(password)
    return password

def validate(password):
    password = password.replace("`", "")
    password = password.replace(";", "")
    password = password.replace('"', "")
    password = password.replace("'", "") 
    password = password.replace(" ", "")
    return password

def get_settings(id, connection):
    cursor = connection.cursor()
    #try:
        # get special symbols' value
    cursor.execute("SELECT specials FROM users WHERE id = " + str(id) + ";")
    spec = cursor.fetchall()
        # get caps' value
    cursor.execute("SELECT caps FROM users WHERE id = " + str(id) + ";")
    up = cursor.fetchall()
    #except:
    #    spec, up = "T", "T"
    if "T" in str(spec):
        spec = True
    else:
        spec = False
    if "T" in str(up):
        up = True
    else:
        up = False
    return spec, up

def set_setting(id, connection, setting, tf):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET " + str(setting) + " = '" + tf + "' WHERE id = " + str(id) + ";")
        connection.commit()
        return f"your {setting} is {tf} now"
    except Error as e:
        print(f'{e}')
        return "something is wrong in changing settings"

id = 491770917# mine id


#password = generate_password(True, False, str(id))

# CLI prototype
# start
# telegram user prints "/start" and bot check does such user exisit
if __name__ == "__main__":
    while True:# cli
        connection = connect()
        cursor = connection.cursor()
        print("what you need? \n[find] - find password by description\n[write] - write new password into database\n[update password] - update already existed password")
        action = input(":")
        if action == "[find]":
            description = input("type description") # search by description
            print(find(description, id))
        elif action == "[write]":
            print("do you want to save old password or generate new one?")
            print("[save old]\n[generate new]")
            new_or_old = input(":")
            if new_or_old == "[save old]":
                password = input("type the password you want to save")
            elif new_or_old == "[generate new]":
                # TODO ask for spesial symbols and caps
                password = generate_password(True, False, str(id))
                print('your password is ' + password)
            else:
                print("something is wrong. :( please try push one of the buttons")
            description = input("type description for your password, for example [facebook.com]")
            print(write(password, description, id, cursor))
        elif action == "[update password]": #update old password
            password = generate_password(True, False, str(id))
            description = input("write something from description")
            print(update_password(password, description, id))
        else:
            print("please tap the button, do not send text")
