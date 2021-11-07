import unittest
from main import *


class password_generator_test(unittest.TestCase):
    def password_generator_test(self):        
        password = ''
        password = generate_password(True, True, "test")
        self.assertGreater(len(password), 30, "password is too small")
        self.assertLessEqual(len(password), 50, "password is too big")



if __name__ == "__main__":
    unittest.main()
