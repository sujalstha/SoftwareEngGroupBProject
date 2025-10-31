import os
import sqlite3
import pytest
import tkinter as tk
from main import PlayerInfoScreen  # assuming your file is named main.py


@pytest.fixture
def setup_db(tmp_path):
    """Create a temporary database path for testing."""
    test_db_path = tmp_path / "test_trivia_data.db"
    yield test_db_path
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture
def setup_player_info(monkeypatch, setup_db):
    """Create a PlayerInfoScreen instance using a temp db."""
    root = tk.Tk()
    player_screen = PlayerInfoScreen(root)

    # Patch the database filename
    monkeypatch.setattr(sqlite3, "connect", lambda _: sqlite3.connect(setup_db))
    return player_screen


def test_save_player_name_creates_db_and_table(setup_player_info, setup_db):
    """Ensure _save_player_name creates the database and saves a record."""
    player = setup_player_info
    player._save_player_name("Jayce")

    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM players")
    result = cursor.fetchone()
    conn.close()

    assert result[0] == "Jayce", "Player name should be saved in database"


def test_start_quiz_with_valid_name(setup_player_info):
    """Ensure start_quiz saves the name and updates the UI."""
    player = setup_player_info
    player.username_entry.insert(0, "Jayce")

    player.start_quiz()
    labels = [child for child in player.root.winfo_children() if isinstance(child, tk.Label)]

    # The last label should greet the user
    assert any("Welcome, Jayce!" in label.cget("text") for label in labels)


def test_start_quiz_with_empty_name(setup_player_info):
    """Ensure start_quiz shows error if name not entered."""
    player = setup_player_info
    player.start_quiz()

    labels = [child for child in player.root.winfo_children() if isinstance(child, tk.Label)]
    assert any("Please enter your name." in label.cget("text") for label in labels)
