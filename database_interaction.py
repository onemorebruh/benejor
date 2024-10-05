from mysql.connector import connect

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE


def DB_execute_query(query: str):
    connection = connect(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWORD,
                         database=DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return


def DB_get_user_settings(user_id: str) -> (bool, bool):
    connection = connect(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWORD,
                         database=DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f'SELECT specials, caps FROM user WHERE id = {user_id};')
    special_symbols, uppercase = cursor.fetchone()
    return bool(special_symbols), bool(uppercase)
