import unittest
from main import *

class write_test(unittest.TestCase):
    def write_test(self):
        print("it works") 
        connection = connect()
        cursor = connection.cursor()
        status = write(password, "TEST", 0, cursor)
        self.assertEqual(status, "succes", "writing failed")

if __name__ == "__main__":
    unittest.main()