from mysql.connector import connect

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
from pass_gen_lib import make_valid, decrypt


def db_execute_query(query: str):
    connection = connect(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWORD,
                         database=DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return


def db_find_passwords_by_name(name: str, user: int) -> dict[str, str]:  # dict(description, password)
    connection = connect(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWORD,
                         database=DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"""SELECT password, description 
        FROM password 
        WHERE user={user} AND 
        description LIKE '%{make_valid(name)}%'""")

    passwords = dict()
    for i, result in enumerate(cursor.fetchall()):
        if result[1] == "":
            passwords[f"empty string {i}"] = result[0]
        else:
            passwords[result[1]] = decrypt(result[0], user)
    return passwords


def db_get_user_settings(user_id: str) -> (bool, bool):
    connection = connect(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWORD,
                         database=DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f'SELECT specials, caps FROM user WHERE id = {user_id};')
    special_symbols, uppercase = cursor.fetchone()
    return bool(special_symbols), bool(uppercase)
