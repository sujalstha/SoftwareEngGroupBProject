import os
import sqlite3
import pytest
import main  # your main.py

TEST_DB = "test_trivia_data.db"

# ---- Minimal fake Tk root so PlayerInfoScreen doesn't crash ----
class FakeRoot:
    def __init__(self):
        self._children = []
    def title(self, *_): pass
    def configure(self, **kwargs): pass
    def winfo_children(self): return self._children

# ---- Patch sqlite to write to a temp file, not trivia_data.db ----
@pytest.fixture()
def setup_temp_db(monkeypatch):
    def fake_connect(_filename):
        # always connect to our test DB
        return sqlite3.connect(TEST_DB)
    monkeypatch.setattr(main.sqlite3, "connect", fake_connect)

    # clean start
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def _fetch_all_names():
    con = sqlite3.connect(TEST_DB)
    try:
        cur = con.cursor()
        cur.execute("SELECT name FROM players")
        return [r[0] for r in cur.fetchall()]
    except sqlite3.OperationalError:
        # table not created yet
        return []
    finally:
        con.close()

def test_player_name_is_stored(setup_temp_db):
    screen = main.PlayerInfoScreen(FakeRoot())
    name = "Sujal"
    screen._save_player_name(name)

    assert _fetch_all_names() == [name]

def test_empty_name_does_not_crash(setup_temp_db):
    screen = main.PlayerInfoScreen(FakeRoot())
    try:
        screen._save_player_name("")  # your code allows insert; we just ensure no crash
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
