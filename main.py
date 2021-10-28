import random
import mysql.connector
from mysql.connector import Error

def connect():
    connection = None
    try:
        connection = mysql.connector.connect( 
            host="127.0.0.1",
            user="tgBot",
            passwd="L3t M3 1n!"
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
        words.split(" ", ", ")
    # cycle plugs words into password list untils it have 50 symbols
    print(password_list)
    password_list = charge(password_list, 50)
    print(password_list, "this is password_list")
    #TODO make random letters Upppder
    random.shuffle(password_list)# mistake is here
    print(password_list, "shuffled list")
    password = ''.join(password_list)
    return password

connect()
#password = generate_password(True, False, False, "bruh")

