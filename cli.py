from functions import *
from config import *

action = ""
password = ""
key = ""
while True:
    print(
        """
        choose action\n
        [0] generate password
        [1] encrypt password
        [2] decrypt password
        """
    )
    action = input("action: ")
    if action == "0":
        print(generate_password(True, True))
    elif action == "1":
        password = input("password: ")
        key = input("key: ")
        print(encrypt(password, int(key)))
    elif action == "2":
        password = input("password: ")
        key = input("key: ")
        print(decrypt(password, int(key)))
    else:
        print("please use correct numbers next time")