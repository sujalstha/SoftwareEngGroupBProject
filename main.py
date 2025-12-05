import random
import tkinter as tk

from DiffSelect import DiffSelect
from generate_trivia import generate_questions_for_difficulty

# OU crimson and cream
OU_CRIMSON = "#841617"
OU_CREAM = "#FDF9D8"

# Time limits per difficulty (in seconds)
TIME_PER_DIFFICULTY = {
    "Easy": 30,
    "Medium": 20,
    "Hard": 10,
}


class StartScreen:
    def __init__(self, root: tk.Tk, diff_manager: DiffSelect):
        self.root = root
        self.diff_manager = diff_manager

        self.root.title("OU Trivia Game")
        self.root.geometry("600x500")
        self.root.configure(bg=OU_CREAM)
        self.root.resizable(False, False)

        main_frame = tk.Frame(root, bg=OU_CREAM)
        main_frame.pack(expand=True, padx=20, pady=20)

        title_main = tk.Label(
            main_frame,
            text="OU Trivia",
            font=("Arial Black", 40),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
        )
        title_main.pack(pady=(0, 10))

        subtitle = tk.Label(
            main_frame,
            text="Test your OU knowledge!",
            font=("Arial", 16, "italic"),
            bg=OU_CREAM,
            fg="black",
        )
        subtitle.pack(pady=10)

        diff_label = tk.Label(
            main_frame,
            text="Select Difficulty:",
            font=("Arial", 16, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        diff_label.pack(pady=(20, 10))

        btn_frame = tk.Frame(main_frame, bg=OU_CREAM)
        btn_frame.pack()

        for level in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(
                btn_frame,
                text=level,
                font=("Arial", 16, "bold"),
                bg=OU_CRIMSON,
                fg="black",
                activebackground="#660000",
                activeforeground="white",
                width=10,
                height=2,
                relief="raised",
                command=lambda l=level: self.start_game(l),
            )
            btn.pack(side="left", padx=10, pady=10)

        exit_button = tk.Button(
            main_frame,
            text="Exit",
            font=("Arial", 14),
            fg="black",
            width=10,
            bg=OU_CRIMSON,
            activebackground="#660000",
            relief="raised",
            command=root.quit,
        )
        exit_button.pack(pady=20)

        self.status_label = tk.Label(
            main_frame,
            text="",
            fg="red",
            bg=OU_CREAM,
            font=("Arial", 12),
        )
        self.status_label.pack(pady=(5, 0))

    def start_game(self, difficulty: str):
        # Save difficulty in DiffSelect
        try:
            self.diff_manager.difficulty_level_sel(difficulty)
        except ValueError as e:
            self.status_label.config(text=str(e))
            return

        # Let user know we are generating questions
        self.status_label.config(text=f"Generating {difficulty} questions... please wait.")
        self.root.update_idletasks()

        # Call the generator (this overwrites the JSON file each time)
        try:
            questions = generate_questions_for_difficulty(difficulty)
        except Exception as e:
            self.status_label.config(text=f"Error generating questions: {e}")
            return

        if not questions:
            self.status_label.config(
                text=f"No questions were generated. Check URLs or API key."
            )
            return

        # Shuffle questions to vary order
        random.shuffle(questions)

        # Clear the window and go to quiz screen
        for widget in self.root.winfo_children():
            widget.destroy()
        QuizScreen(self.root, questions, difficulty)


class QuizScreen:
    def __init__(self, root: tk.Tk, questions, difficulty: str):
        self.root = root
        self.questions = questions
        self.difficulty = difficulty
        self.current_index = 0
        self.streak = 0
        self.timer_id = None
        self.remaining_time = TIME_PER_DIFFICULTY.get(difficulty, 30)

        self.root.title(f"OU Trivia — {difficulty} mode")
        self.root.configure(bg=OU_CREAM)

        # Layout frames
        self.main_frame = tk.Frame(self.root, bg=OU_CREAM)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Top info: difficulty, timer, streak
        self.info_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        self.info_frame.pack(fill="x", pady=(0, 10))

        self.diff_label = tk.Label(
            self.info_frame,
            text=f"Difficulty: {self.difficulty}",
            font=("Arial", 14, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        self.diff_label.pack(side="left")

        self.timer_label = tk.Label(
            self.info_frame,
            text="Time: --",
            font=("Arial", 14, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        self.timer_label.pack(side="left", padx=20)

        self.streak_label = tk.Label(
            self.info_frame,
            text="Streak: 0",
            font=("Arial", 14, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        self.streak_label.pack(side="right")

        # Question text
        self.question_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 18, "bold"),
            bg=OU_CREAM,
            fg="black",
            wraplength=550,
            justify="center",
        )
        self.question_label.pack(pady=(20, 20))

        # Hint label
        self.hint_label = tk.Label(
            self.main_frame,
            text="Hint: ",
            font=("Arial", 12, "italic"),
            bg=OU_CREAM,
            fg="black",
            wraplength=550,
            justify="center",
        )
        self.hint_label.pack(pady=(0, 10))

        # Answer buttons
        self.buttons_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        self.buttons_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text=f"Option {i+1}",
                font=("Arial", 14),
                bg=OU_CRIMSON,
                fg="black",
                activebackground="#660000",
                activeforeground="white",
                width=25,
                height=2,
                wraplength=400,
                justify="center",
                command=lambda idx=i: self.handle_answer(idx),
            )
            btn.grid(row=i, column=0, pady=5)
            self.option_buttons.append(btn)

        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 12),
            bg=OU_CREAM,
            fg="black",
        )
        self.status_label.pack(pady=(10, 0))

        self.load_question()

    # ---------------- Timer logic ----------------

    def start_timer(self):
        self.remaining_time = TIME_PER_DIFFICULTY.get(self.difficulty, 30)
        self.update_timer_label()
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.timer_id = self.root.after(1000, self._tick)

    def _tick(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.update_timer_label()
            self.game_over("Time's up! Game end.")
            return

        self.update_timer_label()
        self.timer_id = self.root.after(1000, self._tick)

    def update_timer_label(self):
        self.timer_label.config(text=f"Time: {self.remaining_time}s")

    # ---------------- Question logic ----------------

    def load_question(self):
        if self.current_index >= len(self.questions):
            self.you_win()
            return

        q = self.questions[self.current_index]

        self.question_label.config(text=q["question"])
        self.hint_label.config(text=f"Hint: {q.get('hint', '')}")
        self.status_label.config(text="")

        answers = q["answers"]
        for i, btn in enumerate(self.option_buttons):
            if i < len(answers):
                btn.config(text=answers[i], state="normal")
            else:
                btn.config(text="", state="disabled")

        self.update_streak_label()
        self.start_timer()

    def handle_answer(self, idx: int):
        # Stop timer during processing
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        q = self.questions[self.current_index]
        correct_idx = q["correct_index"]

        if idx == correct_idx:
            self.streak += 1
            self.status_label.config(text="Correct!", fg="green")
            self.update_streak_label()
            self._maybe_show_streak_popup()
            self.current_index += 1
            self.root.after(500, self.load_question)
        else:
            self.game_over("Wrong answer! Game end.")

    def update_streak_label(self):
        self.streak_label.config(text=f"Streak: {self.streak}")

    def _maybe_show_streak_popup(self):
        # Show popup for 5, 10, 15 in a row
        if self.streak in (5, 10, 15):
            popup = tk.Toplevel(self.root)
            popup.title("Streak!")
            popup.configure(bg=OU_CREAM)
            popup.geometry("300x150")

            msg = tk.Label(
                popup,
                text=f"{self.streak} in a row!",
                font=("Arial Black", 18),
                bg=OU_CREAM,
                fg=OU_CRIMSON,
            )
            msg.pack(expand=True, pady=20)

            ok_btn = tk.Button(
                popup,
                text="Keep Going",
                font=("Arial", 12, "bold"),
                bg=OU_CRIMSON,
                fg="black",
                activebackground="#660000",
                command=popup.destroy,
            )
            ok_btn.pack(pady=10)

    # ---------------- End states ----------------

    def disable_all_buttons(self):
        for btn in self.option_buttons:
            btn.config(state="disabled")

    def game_over(self, message: str):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.disable_all_buttons()
        self.status_label.config(text=message, fg="red")

        end_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        end_frame.pack(pady=20)

        final_label = tk.Label(
            end_frame,
            text=f"Final streak: {self.streak}",
            font=("Arial", 14, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        final_label.pack(pady=5)

        exit_btn = tk.Button(
            end_frame,
            text="Exit Game",
            font=("Arial", 12, "bold"),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            command=self.root.quit,
        )
        exit_btn.pack(pady=5)

    def you_win(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.disable_all_buttons()
        self.status_label.config(
            text="End game – you win!",
            fg="green",
        )

        end_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        end_frame.pack(pady=20)

        final_label = tk.Label(
            end_frame,
            text=f"You answered all questions!\nFinal streak: {self.streak}",
            font=("Arial", 14, "bold"),
            bg=OU_CREAM,
            fg="black",
            justify="center",
        )
        final_label.pack(pady=5)

        exit_btn = tk.Button(
            end_frame,
            text="Exit Game",
            font=("Arial", 12, "bold"),
            bg=OU_CRIMSON,
            fg="black",
            activebackground="#660000",
            command=self.root.quit,
        )
        exit_btn.pack(pady=5)


# --------- Main entry ---------
if __name__ == "__main__":
    root = tk.Tk()
    diff_manager = DiffSelect()
    StartScreen(root, diff_manager)
    root.mainloop()
