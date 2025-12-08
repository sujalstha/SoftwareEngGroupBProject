import sqlite3
import hashlib
import os

# Global instance required for test access
_GLOBAL_AUTH = None


class AuthDB:
    def __init__(self, db_path="users.db"):
        """
        Initialize the authentication database.
        db_path can be a filename or ':memory:' for testing.
        """
        self.db_path = db_path

        # Persistent connection (CRUCIAL for :memory:)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        self._create_table()

    def _create_table(self):
        """Create the users table if it does not already exist."""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt BLOB NOT NULL
            )
        """)
        self.conn.commit()

    def hash_password(self, password, salt):
        """Return SHA-256 hash of (salt + password)."""
        return hashlib.sha256(salt + password.encode()).hexdigest()

    def create_user(self, username, password):
        """
        Create a new user.
        Returns True on success, False if username already exists.
        """
        salt = os.urandom(16)
        hashed = self.hash_password(password, salt)

        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, hashed, salt),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        """
        Verify a user's password.
        Returns True if correct, False otherwise.
        """
        cur = self.conn.cursor()
        cur.execute(
            "SELECT password_hash, salt FROM users WHERE username=?",
            (username,)
        )
        row = cur.fetchone()

        if row is None:
            return False

        stored_hash = row["password_hash"]
        salt = row["salt"]

        return stored_hash == self.hash_password(password, salt)

def init_db(path=":memory:"):
    """
    Initialize a global database instance.
    Tests always call this before get_conn().
    """
    global _GLOBAL_AUTH
    _GLOBAL_AUTH = AuthDB(path)
    return _GLOBAL_AUTH


def get_conn():
    """
    Return the SQLite connection for tests.
    """
    if _GLOBAL_AUTH is None:
        raise RuntimeError("ERROR: init_db() must be called before get_conn().")
    return _GLOBAL_AUTH.conn
