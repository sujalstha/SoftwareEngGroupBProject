import unittest
import os
import sys

# Ensure Python imports the login_hashing.py located in THIS FOLDER
sys.path.append(os.path.dirname(__file__))

import login_hashing as auth


class TestLoginHashing(unittest.TestCase):

    def setUp(self):
        # Initialize a clean in-memory database for each test
        auth.init_db(":memory:")
        self.conn = auth.get_conn()

    def test_create_user(self):
        self.assertTrue(auth._GLOBAL_AUTH.create_user("alice", "password123"))

    def test_duplicate_user(self):
        auth._GLOBAL_AUTH.create_user("bob", "mypassword")
        self.assertFalse(auth._GLOBAL_AUTH.create_user("bob", "anotherpass"))

    def test_verify_correct(self):
        auth._GLOBAL_AUTH.create_user("charlie", "mypassword")
        self.assertTrue(auth._GLOBAL_AUTH.verify_user("charlie", "mypassword"))

    def test_verify_wrong(self):
        auth._GLOBAL_AUTH.create_user("dave", "rightpass")
        self.assertFalse(auth._GLOBAL_AUTH.verify_user("dave", "wrongpass"))

    def test_verify_nonexistent_user(self):
        self.assertFalse(auth._GLOBAL_AUTH.verify_user("ghost", "whatever"))


if __name__ == "__main__":
    unittest.main()
