"""

OU TRIVIA APP
ID: Group B
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
        self.root.title("Enter Your Name")
        self.root.configure(bg=OU_CREAM)

        # Enter your Name Text
        tk.Label(self.root, text="Enter your Name", font=("Arial Black", 20),
                 fg=OU_CRIMSON, bg=OU_CREAM).place(relx=0.5, rely=0.4, anchor='center')

        # Name Entry and Black Border
        self.username_entry = tk.Entry(self.root, width=30, font=("Arial", 14), bg="white", borderwidth=2,
                                       relief="solid", highlightthickness=1, highlightbackground="black")
        self.username_entry.place(relx=0.5, rely=0.5, anchor='center')

        # Bug fix name entry reloads on focus as window opens (DO NOT REMOVE!)
        self.username_entry.focus_set()

        self.start_button = tk.Button(self.root, text="Start Quiz", font=("Arial", 16, "bold"),
                                      bg=OU_CRIMSON, fg="black", activebackground="#660000",
                                      activeforeground="white", width=15, height=2,
                                      relief="raised", command=self.start_quiz)
        self.start_button.place(relx=0.5, rely=0.6, anchor='center')


    def _save_player_name(self, name):
            try:
                # Database file is named 'trivia_data.db'
                conn = sqlite3.connect('trivia_data.db')
                cursor = conn.cursor()

                # Create a table to store names
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS players
                               (
                                   id
                                   INTEGER
                                   PRIMARY
                                   KEY,
                                   name
                                   TEXT
                                   NOT
                                   NULL
                               )
                               ''')

                # Inserts player's name into the table
                cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
                conn.commit()
                print(f"{name} saved to the database")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            finally:
                if 'conn' in locals() and conn:
                    conn.close()

    def start_quiz(self):
        player_name = self.username_entry.get().strip()

        if player_name:
            self._save_player_name(player_name)

            for widget in self.root.winfo_children():
                widget.destroy()
            tk.Label(self.root, text=f"Welcome, {player_name}!\nQuiz starting soon...",
                     font=("Arial", 20), bg=OU_CREAM, fg="black").pack(expand=True)
        else:
            # Case where name not entered
            tk.Label(self.root, text="Please enter your name.", fg="red", bg=OU_CREAM).place(relx=0.5, rely=0.7,
                                                                                             anchor='center')

if __name__ == "__main__":
    root = tk.Tk()
    app = StartScreen(root)
    root.mainloop()