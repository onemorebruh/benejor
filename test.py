import unittest
import time

from functions import *
from config import *


class test_(unittest.TestCase):
    def test_password_generator_(self):
        password = ''
        password = generate_password(True, True)
        self.assertGreater(len(password), 8, "password is too small")
        self.assertLessEqual(len(password), 66, "password is too big")

    #    def test_create_user_(self):
    #        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    #        result = create_user(0, connection)
    #        self.assertEqual(result, "success")

    def test_find_(self):
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        cursor = connection.cursor()
        arr = find("TEST", 0, connection)
        self.assertIsNotNone(arr, "finding failed")

    def test_write_(self):
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        cursor = connection.cursor()
        password = generate_password(True, True)
        status = write(password, "TEST", 0, connection)
        self.assertEqual(status, "success", "writing failed")

    def test_update_password_(self):
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        cursor = connection.cursor()
        password = generate_password(True, True)
        status = update_password(password, "TEST", 0, connection)
        self.assertEqual(status, "success", "updating failed")

    def test_get_settings_(self):
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        test_spec, test_up = get_settings(0, connection)
        self.assertTrue(test_spec, "you have got the wrong data from database")
        # isBool
        try:
            self.assertTrue(test_up, "you have got the wrong data from database")
        except IndexError:
            self.assertFalse(test_up, "you have got the wrong data from database")

    def test_validator_(self):
        password = "'`; SAILhemetalGAVEthatWIND$wirefewsmallchildCLASSfood"
        self.assertNotIn(password, " ", "password have space in it")
        self.assertNotIn(password, "`", "password have ` in it")
        self.assertNotIn(password, ";", "password have ; in it")
        self.assertNotIn(password, "'", "password have ' in it")
        self.assertNotIn(password, '"', 'password have " in it')

    def test_set_setting_(self):
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        connection = connect(host, user, passwd, database)
        status = set_setting(0, connection, "caps", "F")
        self.assertIsNot(status, "something is wrong in changing settings")

        #    def test_delete_user_(self):
        #        time.sleep(3)
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)

    #        connection = connect(host, user, passwd, database)
    #        result = delete_user(0, connection)
    #        self.assertEqual(result, "success")

    def test_encrypt_(self):
        encoded_data = encrypt("test message", 491770917)
        self.assertEqual(encoded_data, "120c110c116c123c39c109c110c116c122c101c112c102c")

    def test_decrypt_(self):
        decoded_data = decrypt("120c110c116c123c39c109c110c116c122c101c112c102c", 491770917)
        self.assertEqual(decoded_data, "test message")


if __name__ == "__main__":
    unittest.main()
