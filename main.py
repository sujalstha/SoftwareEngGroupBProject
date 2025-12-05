import random
import threading
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

        # threading-related state
        self.worker_thread = None
        self.generated_questions = None
        self.worker_error = None
        self.chosen_difficulty = None

        self.root.title("OU Trivia Game")
        self.root.geometry("900x650")  # bigger window so text fits
        self.root.configure(bg=OU_CREAM)
        self.root.resizable(False, False)

        main_frame = tk.Frame(root, bg=OU_CREAM)
        main_frame.pack(expand=True, padx=20, pady=20, fill="both")

        title_main = tk.Label(
            main_frame,
            text="OU Trivia",
            font=("Arial Black", 42),
            fg=OU_CRIMSON,
            bg=OU_CREAM,
        )
        title_main.pack(pady=(10, 5))

        subtitle = tk.Label(
            main_frame,
            text="Test your OU knowledge!",
            font=("Arial", 18, "italic"),
            bg=OU_CREAM,
            fg="black",
        )
        subtitle.pack(pady=10)

        diff_label = tk.Label(
            main_frame,
            text="Select Difficulty:",
            font=("Arial", 18, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        diff_label.pack(pady=(30, 10))

        btn_frame = tk.Frame(main_frame, bg=OU_CREAM)
        btn_frame.pack()

        self.diff_buttons = []
        for level in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(
                btn_frame,
                text=level,
                font=("Arial", 18, "bold"),
                bg=OU_CRIMSON,
                fg="white",
                activebackground="#660000",
                activeforeground="white",
                width=12,
                height=2,
                relief="raised",
                command=lambda l=level: self.start_game(l),
            )
            btn.pack(side="left", padx=15, pady=10)
            self.diff_buttons.append(btn)

        exit_button = tk.Button(
            main_frame,
            text="Exit",
            font=("Arial", 16),
            fg="white",
            width=12,
            bg=OU_CRIMSON,
            activebackground="#660000",
            relief="raised",
            command=root.quit,
        )
        exit_button.pack(pady=25)

        self.status_label = tk.Label(
            main_frame,
            text="",
            fg="red",
            bg=OU_CREAM,
            font=("Arial", 13),
        )
        self.status_label.pack(pady=(5, 0))

    # -------- difficulty click → start worker thread --------

    def start_game(self, difficulty: str):
        # If a worker is already running, ignore extra clicks
        if self.worker_thread is not None and self.worker_thread.is_alive():
            return

        # Save difficulty in DiffSelect
        try:
            self.diff_manager.difficulty_level_sel(difficulty)
        except ValueError as e:
            self.status_label.config(text=str(e))
            return

        self.chosen_difficulty = difficulty
        self.generated_questions = None
        self.worker_error = None

        # Disable difficulty buttons while loading
        for btn in self.diff_buttons:
            btn.config(state="disabled")

        # Show loading message
        self.status_label.config(
            text=f"Generating {difficulty} questions... please wait."
        )
        self.root.update_idletasks()

        # Start background thread to generate questions
        self.worker_thread = threading.Thread(
            target=self._worker_generate, args=(difficulty,), daemon=True
        )
        self.worker_thread.start()

        # Start polling to see when thread is done
        self.root.after(200, self._check_worker_done)

    def _worker_generate(self, difficulty: str):
        """
        Background thread: DO NOT touch any Tk widgets here.
        Just call generate_questions_for_difficulty and store the result.
        """
        try:
            self.generated_questions = generate_questions_for_difficulty(difficulty)
        except Exception as e:
            self.worker_error = str(e)

    def _check_worker_done(self):
        """
        Called periodically on the Tk main thread.
        When the worker finishes, we either show an error
        or launch the QuizScreen.
        """
        if self.worker_thread is None:
            return

        if self.worker_thread.is_alive():
            # Still working -> check again later
            self.root.after(200, self._check_worker_done)
            return

        # Worker finished
        if self.worker_error:
            self.status_label.config(
                text=f"Error generating questions: {self.worker_error}"
            )
            for btn in self.diff_buttons:
                btn.config(state="normal")
            return

        questions = self.generated_questions or []
        if not questions:
            self.status_label.config(
                text=f"No questions were generated. Check URLs or API key."
            )
            for btn in self.diff_buttons:
                btn.config(state="normal")
            return

        # Shuffle questions to vary order
        random.shuffle(questions)

        # Go to quiz screen
        for widget in self.root.winfo_children():
            widget.destroy()
        QuizScreen(self.root, questions, self.chosen_difficulty)


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
        self.main_frame.pack(expand=True, fill="both", padx=25, pady=25)

        # Top info: difficulty, timer, streak
        self.info_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        self.info_frame.pack(fill="x", pady=(0, 10))

        self.diff_label = tk.Label(
            self.info_frame,
            text=f"Difficulty: {self.difficulty}",
            font=("Arial", 16, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        self.diff_label.pack(side="left")

        self.timer_label = tk.Label(
            self.info_frame,
            text="Time: --",
            font=("Arial", 16, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        self.timer_label.pack(side="left", padx=40)

        self.streak_label = tk.Label(
            self.info_frame,
            text="Streak: 0",
            font=("Arial", 16, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        self.streak_label.pack(side="right")

        # Question text
        self.question_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 22, "bold"),
            bg=OU_CREAM,
            fg="black",
            wraplength=800,    # wider so long questions fit
            justify="center",
        )
        self.question_label.pack(pady=(25, 15))

        # Hint label
        self.hint_label = tk.Label(
            self.main_frame,
            text="Hint: ",
            font=("Arial", 14, "italic"),
            bg=OU_CREAM,
            fg="black",
            wraplength=800,
            justify="center",
        )
        self.hint_label.pack(pady=(0, 20))

        # Answer buttons
        self.buttons_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        self.buttons_frame.pack(pady=10, fill="x")

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text=f"Option {i+1}",
                font=("Arial", 14),
                bg=OU_CRIMSON,
                fg="white",
                activebackground="#660000",
                activeforeground="white",
                width=40,
                height=2,
                wraplength=700,  # let answers wrap cleanly
                justify="center",
                command=lambda idx=i: self.handle_answer(idx),
            )
            btn.pack(pady=6, padx=100, fill="x")
            self.option_buttons.append(btn)

        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 14),
            bg=OU_CREAM,
            fg="black",
        )
        self.status_label.pack(pady=(15, 0))

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
            self.game_over("Time's up! Game end. Goodbye!")
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
            # load next question after short delay
            self.root.after(600, self.load_question)
        else:
            # Wrong answer: then show friendly goodbye
            self.game_over("Incorrect choice! Game over. Goodbye!")

    def update_streak_label(self):
        self.streak_label.config(text=f"Streak: {self.streak}")

    def _maybe_show_streak_popup(self):
        # Show popup for 5, 10, 15 in a row
        if self.streak in (5, 10, 15):
            popup = tk.Toplevel(self.root)
            popup.title("Streak!")
            popup.configure(bg=OU_CREAM)
            popup.geometry("320x160")

            msg = tk.Label(
                popup,
                text=f"{self.streak} in a row!",
                font=("Arial Black", 20),
                bg=OU_CREAM,
                fg=OU_CRIMSON,
            )
            msg.pack(expand=True, pady=20)

            ok_btn = tk.Button(
                popup,
                text="Keep Going",
                font=("Arial", 12, "bold"),
                bg=OU_CRIMSON,
                fg="white",
                activebackground="#660000",
                command=popup.destroy,
            )
            ok_btn.pack(pady=10)

    # ---------------- End states ----------------

    def disable_all_buttons(self):
        for btn in self.option_buttons:
            btn.config(state="disabled")

    def hide_buttons(self):
        # hide answer buttons when game ends
        for btn in self.option_buttons:
            btn.pack_forget()

    def game_over(self, message: str):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.disable_all_buttons()
        self.hide_buttons()

        # Big goodbye message
        self.status_label.config(text=message, fg="red", font=("Arial", 16, "bold"))

        end_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        end_frame.pack(pady=30)

        final_label = tk.Label(
            end_frame,
            text=f"Final streak: {self.streak}",
            font=("Arial", 16, "bold"),
            bg=OU_CREAM,
            fg="black",
        )
        final_label.pack(pady=8)

        goodbye_label = tk.Label(
            end_frame,
            text="Thank you for playing OU Trivia!",
            font=("Arial", 14),
            bg=OU_CREAM,
            fg="black",
        )
        goodbye_label.pack(pady=4)

        # Automatically close the window after 2 seconds
        self.root.after(2000, self.root.destroy)

    def you_win(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.disable_all_buttons()
        self.hide_buttons()

        self.status_label.config(
            text="End game – you win!",
            fg="green",
            font=("Arial", 16, "bold"),
        )

        end_frame = tk.Frame(self.main_frame, bg=OU_CREAM)
        end_frame.pack(pady=30)

        final_label = tk.Label(
            end_frame,
            text=f"You answered all questions!\nFinal streak: {self.streak}",
            font=("Arial", 16, "bold"),
            bg=OU_CREAM,
            fg="black",
            justify="center",
        )
        final_label.pack(pady=8)

        goodbye_label = tk.Label(
            end_frame,
            text="Thank you for playing OU Trivia!",
            font=("Arial", 14),
            bg=OU_CREAM,
            fg="black",
        )
        goodbye_label.pack(pady=4)

        # Close after a short delay
        self.root.after(2500, self.root.destroy)


# --------- Main entry ---------
if __name__ == "__main__":
    root = tk.Tk()
    diff_manager = DiffSelect()
    StartScreen(root, diff_manager)
    root.mainloop()
