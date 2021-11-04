import unittest
from main import generate_password, charge

class password_generator_test(unittest.TestCase):
    def password_generator_test(self):
        password = generate_password(True, True, "test")
        print("password is", len(password), "symbols long")
        self.assertGreater(len(password), 30, "password is too small")
        self.assertLessEqual(len(password), 50, "password is too big")
        print("everything is great")

    #the rest tests

if __name__ == "__main__":
    unittest.main()
