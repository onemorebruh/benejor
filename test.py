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
        
if __name__ == "__main__":
    unittest.main()
