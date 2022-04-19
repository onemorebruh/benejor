import mysql.connector
import sys
from functions import *
from config import *

path = sys.argv[1]
connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
cursor = connection.cursor()
words = open(path).read()
words = words.split("\n")
len_words = len(words)
errors = 0
for each in words:
    try:
        cursor.execute("INSERT INTO dictionary (word) VALUES ('" + each + "');")
        connection.commit()
    except IndexError:
        print(each, "was not accessed into db")
        errors += 1
print(str(len_words - errors) + " words was added successfully")
