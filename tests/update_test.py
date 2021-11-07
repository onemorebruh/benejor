import unittest
from main import *

class write_test(unittest.TestCase):
   def update_password_test(self):
        connection = connect()
        cursor = connection.cursor()
        password = generate_password()
        status = update_password(password, "TEST", 0)
        self.assertEqual(status, "succes", "updating failed") 

if __name__ == "__main__":
    unittest.main()