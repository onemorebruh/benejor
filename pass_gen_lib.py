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
import random
from config import *

dictionary = []


# password generator

def charge(list_of_elements: list, maximum: int, caps: int) -> str:
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
        if caps == 1:
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
    return list_of_elements  # success


def generate_password(special_symbols: int, caps: int) -> str:
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
    if special_symbols == 1:
        number = random.randint(0, int(len(specials) - 1))
        password_list.append(specials[number])
    random.shuffle(password_list)  # mistake is here
    password = ''.join(password_list)
    return password


def validate(password: str) -> str:
    password = password.replace("`", "")
    password = password.replace(";", "")
    password = password.replace('"', "")
    password = password.replace("'", "")
    password = password.replace(" ", "")
    return password


# using database

def connect(host: str, user: str, passwd: str, database: str) -> mysql.connector.connection:
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


# crypting

def encrypt(data: str, key:int) -> str:
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
        crypted_data[i] = str(crypted_data[i]) + random.choice(["A", "B", "C", "D", "E", "F"])
        i += 1
    encoded_data = str(crypted_data)
    encoded_data = validate(encoded_data)
    encoded_data = encoded_data.replace("[", "").replace("]", "").replace(",", "")
    return encoded_data


def decrypt(data: str, key: int) -> str:
    key = [int(x) for x in str(key)]
    i = 0
    j = 0
    # convert string to array of numbers
    encrypted_data = data.replace("A", " ").replace("B", " ").replace("C", " ").replace("D", " ").replace("E", " ").replace("F", " ")
    encrypted_data = encrypted_data.split(" ")
    # math changes numbers to correct number for each sign
    while i < (len(encrypted_data) - 1):
        if j >= len(key):
            j = 0
        encrypted_data[i] = chr(int(encrypted_data[i]) - key[j])
        j += 1
        i += 1
    encrypted_data = str(encrypted_data).replace("[", "").replace("]", "").replace(", ", "").replace("'", "")
    return encrypted_data
