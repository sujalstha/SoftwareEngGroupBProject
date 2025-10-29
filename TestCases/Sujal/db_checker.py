# db_checker.py
import sqlite3

class DBChecker:
    """Standalone SQLite DB checker for your OU Trivia App."""

    def __init__(self, db_file: str = "trivia_data.db"):
        self.db_file = db_file

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def ensure_min_schema(self):
        """Create the players table if it doesn't exist."""
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    name TEXT NOT NULL
                )
            """)
            con.commit()

    def table_exists(self) -> bool:
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
            return cur.fetchone() is not None

    def has_required_columns(self) -> bool:
        """Check that the table has a 'name' column."""
        if not self.table_exists():
            return False
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("PRAGMA table_info(players)")
            cols = {row[1] for row in cur.fetchall()}
            return "name" in cols

    def insert_name(self, name: str):
        """Insert player name (ignores blanks)."""
        if not name:
            return
        self.ensure_min_schema()
        with self._connect() as con:
            con.execute("INSERT INTO players (name) VALUES (?)", (name,))
            con.commit()

    def get_all_names(self):
        """Return all player names (sorted)."""
        if not self.table_exists():
            return []
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM players ORDER BY name ASC")
            return [r[0] for r in cur.fetchall()]

    def wipe(self):
        """Delete all players but keep the table."""
        if not self.table_exists():
            return
        with self._connect() as con:
            con.execute("DELETE FROM players")
            con.commit()


if __name__ == "__main__":
    # Handy manual checker
    db = DBChecker()
    db.ensure_min_schema()
    print("WORKS Table exists:", db.table_exists())
    print("WORKS Has 'name' column:", db.has_required_columns())
    print("Current players:", db.get_all_names() or "None yet")
