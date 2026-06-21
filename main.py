# Import tkinter for creating the main GUI window
import tkinter as tk

# Import to get main.py directory
import os
import sys

# Save the absolute path of the program files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Change working directory
os.chdir(BASE_DIR)

# Fix any importing issues
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# Import the login window interface
from ui.login_window import LoginWindow

# Import authentication service (used by the login system)
from services.auth_service import AuthService


# ================= Main Application Function =================
# This function starts the GUI application
def main():

    # Create the main Tkinter root window
    root = tk.Tk()

    # Open the login window inside the root window
    LoginWindow(root)

    # Start the Tkinter event loop
    # This keeps the GUI running and listening for user actions
    root.mainloop()


# ================= Program Entry Point =================
# This ensures the code runs only when the file is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()
