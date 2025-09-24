"""
CS 2302
ID: GORUP B
OU TRIVIA APP
By Sujal, Joel, Devin, Jayce, Mo, Ryan, Abraham

"""

# libraries needed for the application
import tkinter as tk


# OU crimson and cream
OU_CRIMSON = "#841617"
OU_CREAM = "#FDF9D8"

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("OU Trivia Game")
        self.root.geometry("500x500")
        self.root.configure(bg=OU_CREAM)

        # Title Text
        self.title_shadow = tk.Label(root, text="OU Trivia", font=("Arial Black", 36),
                                     fg="black", bg=OU_CREAM)

        self.title_main = tk.Label(root, text="OU Trivia", font=("Arial Black", 36),
                                   fg=OU_CRIMSON, bg=OU_CREAM)
        self.title_main.place(x=150, y=90)

        # subtitles
        self.subtitle = tk.Label(root, text="Test your OU knowledge!",
                                 font=("Arial", 16, "italic"), bg=OU_CREAM, fg="black")
        self.subtitle.pack(pady=160)

        # start button
        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 18, "bold"),
                                      bg=OU_CRIMSON, fg="black", activebackground="#660000",
                                      activeforeground="white", width=12, height=2,
                                      relief="raised", command=self.start_game)
        self.start_button.pack(pady=20)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 14),
                                     fg="black", width=10, bg=OU_CRIMSON,
                                     activebackground="#660000",
                                     relief="raised", command=root.quit)
        self.exit_button.pack(pady=10)

    def start_game(self):
        # clear screen for new window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Game Starting Soon...", font=("Arial Black", 20),
                 fg=OU_CRIMSON, bg=OU_CREAM).pack(expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = StartScreen(root)
    root.mainloop()
