import unittest
from main import *
from config import *

class test_(unittest.TestCase):
    def test_password_generator_(self):        
        password = ''
        password = generate_password(True, True, "test")
        self.assertGreater(len(password), 30, "password is too small")
        self.assertLessEqual(len(password), 50, "password is too big")

    def test_find_(self):
        connection = connect(host, user, passwd, database)
        cursor = connection.cursor()
        arr = find("TEST", 0, connection)
        self.assertIsNotNone( arr, "finding failed") 

    def test_write_(self):
        print("it works") 
        connection = connect(host, user, passwd, database)
        cursor = connection.cursor()
        password = generate_password(True, True, "test")
        status = write(password, "TEST", 0, connection)
        self.assertEqual(status, "succes", "writing failed")

    def test_update_password_(self):
        connection = connect(host, user, passwd, database)
        cursor = connection.cursor()
        password = generate_password(True, True, "test")
        status = update_password(password, "TEST", 0, connection)
        self.assertEqual(status, "succes", "updating failed") 

    def test_get_settings_(self):
        connection = connect(host, user, passwd, database)
        test_spec, test_up = get_settings(0, connection)
        self.assertTrue(test_spec, "you have got the wrong data from database")
        self.assertTrue(test_up, "you have got the wrong data from database")

    def test_validator_(self):
        password = "'`; SAILhemetalGAVEthatWIND$wirefewsmallchildCLASSfood"
        password = validate(password)
        self.assertNotIn(password, " ", "password have space in it")
        self.assertNotIn(password, "`", "password have ` in it")
        self.assertNotIn(password, ";", "password have ; in it")
        self.assertNotIn(password, "'", "password have ' in it")
        self.assertNotIn(password, '"', 'password have " in it')

    def test_set_setting(self):
        connection = connect(host, user, passwd, database)
        status = set_setting(0, connection, "caps", "F")
        self.assertIsNot(status, "something is wrong in changing settings")

if __name__ == "__main__":
    unittest.main()
