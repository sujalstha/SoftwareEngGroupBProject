import tkinter as tk
from generate_trivia import get_random_question

OU_CRIMSON = "#841617"
OU_CREAM = "#FDF9D8"


class StreakManager:
    def __init__(self):
        self.streak = 0

    def correct(self):
        """Increase streak by +5 for every correct answer."""
        self.streak += 5
        return self.streak

    def wrong(self):
        """Reset streak to zero when user answers incorrectly."""
        self.streak = 0
        return self.streak


class QuizScreen:
    def __init__(self, root, db, player_name, diff_manager):
        self.root = root
        self.db = db
        self.player_name = player_name
        self.diff_manager = diff_manager

        # Create a streak manager for this player/session
        self.streak_mgr = StreakManager()

        # Prepare GUI
        for w in root.winfo_children():
            w.destroy()

        self.root.title("OU Trivia Quiz")
        self.root.configure(bg=OU_CREAM)

        self.frame = tk.Frame(self.root, bg=OU_CREAM)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Streak label (updates live)
        self.streak_label = tk.Label(
            self.frame,
            text="Streak: 0",
            font=("Arial", 16, "bold"),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
        )
        self.streak_label.pack(pady=10)

        # Load first question
        self.load_question()

    def load_question(self):
        """Clears old question and loads a new question."""
        for w in self.frame.winfo_children():
            if w is not self.streak_label:
                w.destroy()

        q = get_random_question()
        self.current_question = q

        # Show question
        tk.Label(
            self.frame,
            text=q["question"],
            wraplength=420,
            font=("Arial", 18, "bold"),
            bg=OU_CREAM,
        ).pack(pady=10)

        # Show answer buttons
        for idx, option in enumerate(q["options"]):
            tk.Button(
                self.frame,
                text=option,
                font=("Arial", 14),
                bg=OU_CRIMSON,
                fg="black",
                width=26,
                height=2,
                command=lambda i=idx: self.check_answer(i),
            ).pack(pady=5)

        # Show hint
        tk.Label(
            self.frame,
            text=f"Hint: {q['hint']}",
            font=("Arial", 12, "italic"),
            bg=OU_CREAM,
        ).pack(pady=15)

    def check_answer(self, selected_index):
        """Handle user answer selection."""
        correct_index = self.current_question["correct_index"]

        if selected_index == correct_index:
            new_streak = self.streak_mgr.correct()
            self.streak_label.config(text=f"🔥 Streak: {new_streak}")
        else:
            self.streak_mgr.wrong()
            self.streak_label.config(text="Streak: 0")

        # Load next question
        self.load_question()
