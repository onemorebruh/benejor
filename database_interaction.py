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
