import unittest
import time

from pass_gen_lib import *
from config import *


class test_pass_gen_lib(unittest.TestCase):
    def test_password_generator_(self):
        password = ''
        password = generate_password(True, True)
        self.assertGreater(len(password), 8, "password is too small")
        self.assertLessEqual(len(password), 66, "password is too big")

    def test_encrypt_(self):
        encoded_data = encrypt("ANYREPEAT%themSQUARESENDleadtouch", 491770917)  # encrypt
        # do stuff for comparing only
        encoded_data = encoded_data.replace("A", " ").replace("B", " ").replace("C", " ").replace("D", " ").replace("E",
                                                                                                                    " ").replace(
            "F", " ")
        encoded_data = encoded_data.split(" ")
        self.assertEqual(encoded_data,
                         ['69', '87', '90', '89', '76', '80', '78', '66', '91', '41', '125', '105', '108', '116', '83',
                          '90', '86', '72', '86', '78', '84', '76', '85', '68', '117', '102', '104', '104', '125',
                          '112', '124', '106', '104', ''])

    def test_decrypt_(self):
        decoded_data = decrypt(
            "69E87A90A89F76A80A78B66B91C41A125F105A108D116F83F90D86A72B86F78A84E76C85A68F117E102F104A104B125A112A124B106F104C",
            491770917)
        self.assertEqual(decoded_data, "ANYREPEAT%themSQUARESENDleadtouch")


if __name__ == "__main__":
    unittest.main()
