import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import AuthService
from ui.store_window import StoreWindow
from ui.admin_panel import AdminPanel
from ui.style import setup_style
from ui.utils import center_window


class LoginWindow:
    # This class handles the login and registration window

    def __init__(self, root):
        # Store the main root window
        self.root = root

        # Set window title
        self.root.title("Online Shop Login")

        # Center the window on screen
        center_window(self.root, 430, 330)

        # Apply custom UI styles
        setup_style(self.root)

        # Build the user interface
        self.build_ui()

    def build_ui(self):
        # Create main frame with padding
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        # Username label
        ttk.Label(
            frame,
            text="Username"
        ).grid(row=0, column=0, pady=5, sticky="w")

        # Username entry field
        self.username = ttk.Entry(frame, width=25)
        self.username.grid(row=0, column=1, pady=5)

        # Password label
        ttk.Label(
            frame,
            text="Password"
        ).grid(row=1, column=0, pady=5, sticky="w")

        # Password entry field (hidden characters)
        self.password = ttk.Entry(frame, show="*", width=25)
        self.password.grid(row=1, column=1, pady=5)

        # Login button
        ttk.Button(
            frame,
            text="Login",
            command=self.login
        ).grid(row=2, column=0, columnspan=2, pady=12)

        # Register button
        ttk.Button(
            frame,
            text="Register",
            command=self.register
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Exit button to close the application
        ttk.Button(
            frame,
            text="Exit",
            command=self.root.destroy
        ).grid(row=4, column=0, columnspan=2, pady=5)

    def login(self):
        # Get entered username and password
        username = self.username.get().strip()
        password = self.password.get().strip()

        # Check if fields are empty
        if username == "" or password == "":
            messagebox.showwarning("Warning", "Enter username and password.")
            return

        # Attempt login using AuthService
        user = AuthService.login(username, password)

        # If login fails
        if user is None:
            messagebox.showerror("Error", "Invalid username or password.")
            return

        # Hide login window after successful login
        self.root.withdraw()

        # Open admin panel if user is admin
        if user[3] == "Admin":
            AdminPanel(self.root, user)
        else:
            # Otherwise open the store window for normal users
            StoreWindow(self.root, user)

    def register(self):
        # Get entered username and password
        username = self.username.get().strip()
        password = self.password.get().strip()

        # Check if fields are empty
        if username == "" or password == "":
            messagebox.showwarning("Warning", "Enter username and password.")
            return

        # Attempt user registration through AuthService
        success, message = AuthService.register(username, password)

        # Show result message
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
