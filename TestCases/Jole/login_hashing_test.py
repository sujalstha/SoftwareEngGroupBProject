import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Security Question')))
import login_hashing as auth  # Adjust path if needed

class TestLoginHashing(unittest.TestCase):
    def setUp(self):
        # Reinitialize database before each test
        if os.path.exists("auth.db"):
            os.remove("auth.db")
        self.db = auth.AuthDB("auth.db")

    def tearDown(self):
        if os.path.exists("auth.db"):
            os.remove("auth.db")

    def test_create_user_success(self):
        """Test that creating a new user works."""
        result = self.db.create_user("alice", "password123")
        self.assertTrue(result, "Creating a new user should succeed")

    def test_create_user_duplicate(self):
        """Test that creating a duplicate user fails."""
        self.db.create_user("bob", "mypassword")
        result = self.db.create_user("bob", "anotherpass")
        self.assertFalse(result, "Creating a duplicate user should fail")

    def test_verify_correct_password(self):
        """Test logging in with correct password."""
        self.db.create_user("charlie", "mypassword")
        result = self.db.verify_user("charlie", "mypassword")
        self.assertTrue(result, "Correct password should verify successfully")

    def test_verify_incorrect_password(self):
        """Test logging in with incorrect password."""
        self.db.create_user("dave", "mypassword")
        result = self.db.verify_user("dave", "wrongpass")
        self.assertFalse(result, "Incorrect password should fail verification")

    def test_verify_nonexistent_user(self):
        """Test logging in with a username that doesn't exist."""
        result = self.db.verify_user("eve", "anyPassword")
        self.assertFalse(result, "Nonexistent user should fail verification")


if __name__ == "__main__":
    unittest.main()
