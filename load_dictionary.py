import mysql.connector
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

connection = connect()
cursor = connection.cursor()
words = open('dependencies/dictionary.txt').read()
words = words.split("\n")
len_words = len(words)
errors = 0
for each in words:
    try:
        cursor.execute("INSERT INTO dictionary (word) VALUES ('" + each + "');")
        connection.commit()
    except:
        print(each, "was not assed into db")
        errors += 1
print(str(len_words - errors) + " words was added succesfully")
