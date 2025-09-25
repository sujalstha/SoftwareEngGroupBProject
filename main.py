"""

OU TRIVIA APP
ID: Group B
OU TRIVIA APP
By Sujal, Joel, Devin, Jayce, Mo, Ryan, Abraham

"""
import tkinter as tk
import sqlite3

# OU crimson and cream
OU_CRIMSON = "#841617"
OU_CREAM = "#FDF9D8"

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("OU Trivia Game")
        self.root.geometry("500x500")
        self.root.configure(bg=OU_CREAM)

        # Cannot Resize Windows
        self.root.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(root, bg=OU_CREAM)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Title Text
        self.title_main = tk.Label(self.main_frame, text="OU Trivia", font=("Arial Black", 40),
                                   fg=OU_CRIMSON, bg=OU_CREAM)
        self.title_main.pack(pady=(0, 10))

        # Subtitle
        self.subtitle = tk.Label(self.main_frame, text="Test your OU knowledge!",
                                 font=("Arial", 16, "italic"), bg=OU_CREAM, fg="black")
        self.subtitle.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(self.main_frame, text="Start Game", font=("Arial", 18, "bold"),
                                      bg=OU_CRIMSON, fg="black", activebackground="#660000",
                                      activeforeground="white", width=12, height=2,
                                      relief="raised", command=self.start_game)
        self.start_button.pack(pady=20)

        # Exit Button
        self.exit_button = tk.Button(self.main_frame, text="Exit", font=("Arial", 14),
                                     fg="black", width=10, bg=OU_CRIMSON,
                                     activebackground="#660000",
                                     relief="raised", command=root.quit)
        self.exit_button.pack(pady=10)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        PlayerInfoScreen(self.root)


class PlayerInfoScreen:
    def __init__(self, root):
        self.root = root
        tk.Label(self.root, text="Enter your Name", font=("Arial Black", 20),
                 fg=OU_CRIMSON, bg=OU_CREAM).place(relx=0.5, rely=0.4, anchor='center')

        self.username_entry = tk.Entry(self.root, width=30, font=("Arial", 14), borderwidth=2, relief="solid")
        self.username_entry.place(relx=0.5, rely=0.5, anchor='center')

        self.start_button = tk.Button(self.root, text="Start Quiz", font=("Arial", 16, "bold"),
                                      bg=OU_CRIMSON, fg="black", activebackground="#660000",
                                      activeforeground="white", width=15, height=2,
                                      relief="raised")
        self.start_button.place(relx=0.5, rely=0.6, anchor='center')


if __name__ == "__main__":
    root = tk.Tk()
    app = StartScreen(root)
    root.mainloop()
