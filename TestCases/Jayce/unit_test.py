import pytest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
import importlib

@pytest.fixture
def app():
    """Reload the login module fresh for each test."""
    import Login_Button  # ✅ your real filename
    importlib.reload(Login_Button)
    return Login_Button

def test_login_success(app):
    """Check that correct credentials trigger success message and window closes."""
    
    # Mock valid credentials
    app.username_entry.delete(0, tk.END)
    app.username_entry.insert(0, "outrivia")

    app.password_entry.delete(0, tk.END)
    app.password_entry.insert(0, "boomer")

    mock_showinfo = patch.object(messagebox, "showinfo").start()
    mock_destroy = patch.object(app.root, "destroy").start()

    app.login()

    mock_showinfo.assert_called_once_with("Login Successful", "Welcome to Trivia OU!")
    mock_destroy.assert_called_once()

    patch.stopall()

def test_login_failure(app):
    """Check that wrong credentials trigger failure message."""
    
    app.username_entry.delete(0, tk.END)
    app.username_entry.insert(0, "fakeUser")

    app.password_entry.delete(0, tk.END)
    app.password_entry.insert(0, "wrongPass")

    mock_showerror = patch.object(messagebox, "showerror").start()

    app.login()

    mock_showerror.assert_called_once_with("Login Failed", "Invalid username or password")

    patch.stopall()
