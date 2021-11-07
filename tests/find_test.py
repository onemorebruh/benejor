import unittest
from main import *

class write_test(unittest.TestCase):
    def find_test(self):
        connection = connect()
        cursor = connection.cursor()
        arr = find("TEST", 0)
        self.assertIn(password, arr, "finding") 

if __name__ == "__main__":
    unittest.main()