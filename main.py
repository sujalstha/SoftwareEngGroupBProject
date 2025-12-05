"""
OU TRIVIA APP — Minimal progress tracking
Group B: Sujal, Jole, Devin_Test, Jayce, Mo, Ryan, Abraham
"""


import tkinter as tk
import sqlite3
from pathlib import Path
from DiffSelect import DiffSelect


# OU crimson and cream
OU_CRIMSON = "#841617"
OU_CREAM = "#FDF9D8"
DB_PATH = Path("trivia_data.db")


# --------- Data Layer ---------
class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    name TEXT PRIMARY KEY,
                    level INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
                )
                """
            )
            conn.commit()

    def get_or_create_player(self, name: str) -> int:
        name = name.strip()
        if not name:
            raise ValueError("Empty name")
        with self._connect() as conn:
            cur = conn.cursor()
            # Try to fetch existing
            cur.execute("SELECT level FROM players WHERE name = ?", (name,))
            row = cur.fetchone()
            if row:
                return int(row[0])
            # Insert new with default level 1
            cur.execute(
                """
                INSERT INTO players(name, level) VALUES(?, 1)
                """,
                (name,),
            )
            conn.commit()
            return 1

    def update_level(self, name: str, new_level: int) -> None:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE players
                   SET level = ?, updated_at = datetime('now')
                 WHERE name = ?
                """,
                (int(new_level), name),
            )
            conn.commit()

    def get_level(self, name: str) -> int:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT level FROM players WHERE name = ?", (name,))
            row = cur.fetchone()
            return int(row[0]) if row else 1


# --------- UI Screens ---------
class StartScreen:
    def __init__(self, root: tk.Tk, db: Database):
        self.db = db
        self.root = root
        self.root.title("OU Trivia Game")
        self.root.geometry("500x500")
        self.root.configure(bg=OU_CREAM)
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(root, bg=OU_CREAM)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        self.title_main = tk.Label(
            self.main_frame,
            text="OU Trivia",
            font=("Arial Black", 40),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
        )
        self.title_main.pack(pady=(0, 10))

        self.subtitle = tk.Label(
            self.main_frame,
            text="Test your OU knowledge!",
            font=("Arial", 16, "italic"),
            bg=OU_CREAM,
            fg="black",
        )
        self.subtitle.pack(pady=10)

        self.start_button = tk.Button(
            self.main_frame,
            text="Start",
            font=("Arial", 18, "bold"),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            activeforeground="white",
            width=12,
            height=2,
            relief="raised",
            command=self.start_game,
        )
        self.start_button.pack(pady=20)

        self.exit_button = tk.Button(
            self.main_frame,
            text="Exit",
            font=("Arial", 14),
            fg="black",
            width=10,
            bg=OU_CRIMSON,
            activebackground="#660000",
            relief="raised",
            command=root.quit,
        )
        self.exit_button.pack(pady=10)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        PlayerInfoScreen(self.root, self.db, diff_manager)


class PlayerInfoScreen:
    def __init__(self, root: tk.Tk, db: Database, diff_manager: DiffSelect):
        self.db = db
        self.root = root
        self.diff_manager = diff_manager
        self.root.title("Enter Your Name")
        self.root.configure(bg=OU_CREAM)

        tk.Label(
            self.root,
            text="Enter your Name",
            font=("Arial Black", 20),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
        ).place(relx=0.5, rely=0.4, anchor="center")

        self.username_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 14),
            bg="white",
            borderwidth=2,
            relief="solid",
            highlightthickness=1,
            highlightbackground="black",
        )
        self.username_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.username_entry.focus_set()  # keep focus on open

        self.start_button = tk.Button(
            self.root,
            text="Start Quiz",
            font=("Arial", 16, "bold"),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            activeforeground="white",
            width=15,
            height=2,
            relief="raised",
            command=self.start_quiz,
        )
        self.start_button.place(relx=0.5, rely=0.6, anchor="center")

        # Inline error label
        self.error_label = tk.Label(self.root, text="", fg="red", bg=OU_CREAM, font=("Arial", 11))
        self.error_label.place(relx=0.5, rely=0.68, anchor="center")

    def start_quiz(self):
        name = self.username_entry.get().strip()
        if not name:
            self.error_label.config(text="Please enter your name.")
            return
        try:
            level = self.db.get_or_create_player(name)
        except Exception as e:
            self.error_label.config(text=f"Database error: {e}")
            return

        for widget in self.root.winfo_children():
            widget.destroy()
        #LevelScreen(self.root, self.db, name, level)
        DifficultyScreen(self.root, self.db, name, self.diff_manager)

class DifficultyScreen:
    """New screen to select difficulty after entering player name"""
    def __init__(self, root: tk.Tk, db: Database, player_name: str, diff_manager: DiffSelect):
        self.root = root
        self.db = db
        self.player_name = player_name
        self.diff_manager = diff_manager

        self.root.title("Select Difficulty")
        self.root.configure(bg=OU_CREAM)

        tk.Label(
            self.root,
            text=f"Welcome, {player_name}!\nSelect Difficulty:",
            font=("Arial Black", 20),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
            justify="center"
        ).pack(pady=40)

        for level in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(
                self.root,
                text=level,
                font=("Arial", 16, "bold"),
                bg=OU_CRIMSON,
                fg="black",
                width=12,
                height=2,
                command=lambda l=level: self.select_diff(l)
            )
            btn.pack(pady=10)

    def select_diff(self, level):
        try:
            self.diff_manager.difficulty_level_sel(level)
        except ValueError as e:
            print(f"Error selecting difficulty: {e}")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        level_num = self.db.get_or_create_player(self.player_name)
        LevelScreen(self.root, self.db, self.player_name, level_num, self.diff_manager)


class LevelScreen:
    def __init__(self, root: tk.Tk, db: Database, name: str, level: int, diff_manager: DiffSelect):
        self.root = root
        self.db = db
        self.name = name
        self.level = level

        self.root.title("Quiz Progress")
        self.root.configure(bg=OU_CREAM)

        wrapper = tk.Frame(self.root, bg=OU_CREAM)
        wrapper.pack(expand=True, fill="both", padx=20, pady=20)

        self.heading = tk.Label(
            wrapper,
            text=f"Welcome, {self.name}!",
            font=("Arial Black", 26),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
        )
        self.heading.pack(pady=(0, 10))

        self.level_label = tk.Label(
            wrapper,
            text=self._level_text(),
            font=("Arial", 18),
            bg=OU_CREAM,
        )
        self.level_label.pack(pady=(0, 20))

        self.advance_btn = tk.Button(
            wrapper,
            text="Mark level complete →",
            font=("Arial", 16, "bold"),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            activeforeground="white",
            width=22,
            height=2,
            relief="raised",
            command=self._advance_level,
        )
        self.advance_btn.pack(pady=10)

        self.reset_btn = tk.Button(
            wrapper,
            text="Reset to Level 1",
            font=("Arial", 12),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            width=16,
            relief="raised",
            command=self._reset_level,
        )
        self.reset_btn.pack(pady=(6, 16))

        self.status = tk.Label(wrapper, text="", fg="green", bg=OU_CREAM, font=("Arial", 11))
        self.status.pack()

        self.back_btn = tk.Button(
            wrapper,
            text="← Back to Start",
            font=("Arial", 12),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            relief="raised",
            command=self._back_to_start,
        )
        self.back_btn.pack(pady=8)

    def _level_text(self) -> str:
        return f"Current Level: {self.level}"

    def _refresh_level_label(self):
        self.level_label.config(text=self._level_text())

    def _advance_level(self):
        self.level += 1
        self.db.update_level(self.name, self.level)
        self._refresh_level_label()
        self.status.config(text="Progress saved.")

    def _reset_level(self):
        self.level = 1
        self.db.update_level(self.name, self.level)
        self._refresh_level_label()
        self.status.config(text="Progress reset.")

    def _back_to_start(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        StartScreen(self.root, self.db)


# --------- Main ---------
if __name__ == "__main__":
    root = tk.Tk()
    db = Database(DB_PATH)
    diff_manager = DiffSelect()
    app = StartScreen(root, db)
    root.mainloop()
