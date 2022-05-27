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

dictionary = []


# password generator

def charge(list_of_elements: list, maximum: int, caps: bool):
    global host, user, passwd, database
    connection = connect(host, user, passwd, database)
    string = ''.join(list_of_elements)
    the_biggest_element = {"index": 0, "len": 0}
    while len(string) < maximum:
        # add new word
        global dictionary
        if len(dictionary) == 0:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT word FROM dictionary;")
                dictionary = cursor.fetchall()
                print("dictionary is loaded")
            except IndexError:
                dictionary = ["sorry", "database", "does", "not", "work"]

        number = random.randint(0, len(dictionary) - 1)
        # makes the word randomly Upper
        if caps:
            upper = random.choice([True, False])
            if upper:
                list_of_elements.append(str(dictionary[number]).upper())
            else:
                list_of_elements.append(str(dictionary[number]))
        else:
            list_of_elements.append(str(dictionary[number]))
        # check element for being the biggest so programm can fastly delete it if the massive is too big
        if len(dictionary[number]) > the_biggest_element["len"]:
            the_biggest_element['len'] = len(dictionary[number])
            the_biggest_element['index'] = int(len(list_of_elements) - 1)
        # clear the string form old data to plug new data into it
        number = 0
        while len(list_of_elements) > number:
            list_of_elements[number] = list_of_elements[number].replace("'", "").replace("(", "").replace(")",
                                                                                                          "").replace(
                ",", "")
            number += 1
        string = ''.join(list_of_elements)
    if len(string) > maximum:
        try:
            list_of_elements.pop(the_biggest_element['index'])  # works correctly
        except IndexError:
            while len(string) > maximum:
                list_of_elements.pop()
                string = ''.join(list_of_elements)
    print(list_of_elements)
    return list_of_elements  # success


def generate_password(special_symbols: bool, caps: bool):
    # special_symbols - t/f allow it or not

    # preferred words - t/f ask user about the words it wants in password

    # CAPS - t/f should password contain upper and downer letters   # crypting_key - string - crypts the generated
    # password before plugining it into bd and helps to encrypt
    specials = ["!", "#", "$", "%", "&", "(", ")", "*" "+", ",", "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8",
                "9", ":", "<", "=", ">", "?", "_", "@", "[", "]", "{", "}"]
    password_list = []  # it will contain all the symbols
    password = ''
    number = 0  # just for a few tasks
    # cycle plugs words into password list until it have 50 symbols
    password_list = charge(password_list, 32, caps)
    if special_symbols:
        number = random.randint(0, int(len(specials) - 1))
        password_list.append(specials[number])
    random.shuffle(password_list)  # mistake is here
    password = ''.join(password_list)
    print(password)
    return password


def validate(password: str):
    password = password.replace("`", "")
    password = password.replace(";", "")
    password = password.replace('"', "")
    password = password.replace("'", "")
    password = password.replace(" ", "")
    print(password)
    return password


# using database

def connect(host: str, user: str, passwd: str, database: str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
    except Error as e:
        print(f"'{e}'")
    return connection


def write(password: str, description: str, _id: int, connection):
    cursor = connection.cursor()
    date = str(datetime.datetime.today()).split()[0]  # data format for mysql
    password = encrypt(password, _id)
    # sql request
    cursor.execute(
        "INSERT INTO user" + str(_id) + " (date, password, description) VALUES ('" + str(date) + "', '" + str(
            password) + "', '" + str(description) + "');")
    connection.commit()
    return "success"


def find(description: str, _id: int, connection):
    i = 0
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM user" + str(_id) + " WHERE description LIKE'%" + description + "%';")
    found_passwords = cursor.fetchall()
    while i < len(found_passwords):
        found_passwords[i] = str(found_passwords[i]).replace("(", "").replace(")", "").replace("'", "").replace(",", "")
        found_passwords[i] = decrypt(found_passwords[i], _id)
        i += 1
    return found_passwords


def update_password(password: str, description: str, _id: int, connection):
    cursor = connection.cursor()
    date = str(datetime.datetime.today()).split()[0]
    password = encrypt(password, _id)
    try:
        cursor.execute("UPDATE user" + str(
            _id) + " SET password = '" + password + "', date = '" + date + "' WHERE description LIKE '%" + description \
                       + "%';")
        connection.commit()
        return "success"
    except Error as e:
        print(f'{e}')
        return "something is wrong with your description"


def get_settings(_id: int, connection):
    cursor = connection.cursor()
    # try:
    # get special symbols' value
    cursor.execute("SELECT specials FROM users WHERE id = " + str(_id) + ";")
    spec = cursor.fetchall()
    # get caps' value
    cursor.execute("SELECT caps FROM users WHERE id = " + str(_id) + ";")
    up = cursor.fetchall()
    # except:
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


def set_setting(_id: int, connection, setting: str, tf: str):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET " + str(setting) + " = '" + tf + "' WHERE id = " + str(_id) + ";")
        connection.commit()
        return f"your {setting} is {tf} now"
    except Error as e:
        print(f'{e}')
        return "something is wrong in changing settings"


def create_user(_id: int, connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE user" + str(
        _id) + "(id int AUTO_INCREMENT NOT NULL, date date NOT NULL, password varchar(200) NOT NULL, description "
               "varchar(255) DEFAULT NULL, PRIMARY KEY (id));")
    connection.commit()
    cursor.execute("INSERT INTO users (id) VAlUES (" + str(_id) + ");")
    connection.commit()
    return "success"


def delete_user(_id: int, connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE user" + str(_id) + ";")
    connection.commit()
    cursor.execute("DELETE FROM users WHERE id = " + str(_id) + ";")
    connection.commit()
    return "success"


# crypting

def encrypt(data: str, key:int):
    encoded_data = data
    key = [int(x) for x in str(key)]
    i = 0
    j = 0
    crypted_data = []
    while i < len(data):
        if j >= len(key):
            j = 0
        crypted_data.append(ord(encoded_data[i]) + key[j])
        i += 1
        j += 1
    i = 0
    while i < len(crypted_data):
        crypted_data[i] = str(crypted_data[i]) + "c"
        i += 1
    encoded_data = str(crypted_data)
    encoded_data = validate(encoded_data)
    encoded_data = encoded_data.replace("[", "").replace("]", "").replace(",", "")
    return encoded_data


def decrypt(data: str, key: int):
    key = [int(x) for x in str(key)]
    i = 0
    j = 0
    # decrypting 
    encrypted_data = data.split("c")
    print(encrypted_data)
    while i < (len(encrypted_data) - 1):
        if j >= len(key):
            j = 0
        encrypted_data[i] = chr(int(encrypted_data[i]) - key[j])
        j += 1
        i += 1
    encrypted_data = str(encrypted_data).replace("[", "").replace("]", "").replace(", ", "").replace("'", "")
    return encrypted_data
