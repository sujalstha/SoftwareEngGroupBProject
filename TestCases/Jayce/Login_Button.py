
import tkinter as tk
from tkinter import messagebox

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Example credentials — replace with your own logic
    if username == "outrivia" and password == "boomer":
        messagebox.showinfo("Login Successful", "Welcome to Trivia OU!")
        root.destroy()  # Close login window
        # You could open your trivia game window here
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create main window
root = tk.Tk()
root.title("Trivia OU Login")
root.geometry("300x200")
root.config(bg="#841617")  # OU crimson background

# Title
title_label = tk.Label(root, text="Trivia OU Login", bg="#841617", fg="white", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Username
tk.Label(root, text="Username:", bg="#841617", fg="white").pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Password
tk.Label(root, text="Password:", bg="#841617", fg="white").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Login button
login_button = tk.Button(root, text="Login", bg="white", fg="#841617", command=login)
login_button.pack(pady=10)

root.mainloop()
