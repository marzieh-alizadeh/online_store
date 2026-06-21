# Import ttk module for styling Tkinter widgets
from tkinter import ttk


# ================= Color Definitions =================
# Primary color used in some UI elements
PRIMARY = "#93c5fd"      # light blue

# Background color for the main window
BG = "#f8fafc"           # very light slate/blue background

# Card or panel background color
CARD = "#e2e8f0"         # soft slate gray card

# Default text color
TEXT = "#334155"         # slate gray text

# Accent color used for highlights
ACCENT = "#bfdbfe"       # pale blue accent

# Button background color
BUTTON = "#60a5fa"       # soft blue button

# White color for tables and fields
WHITE = "#ffffff"


def setup_style(root):
    # Create a style object connected to the main Tk root
    style = ttk.Style(root)

    # Try to use the "clam" theme (modern looking)
    try:
        style.theme_use("clam")
    except:
        # If theme is not available ignore the error
        pass

    # ================= Frame Style =================
    # Default frame background
    style.configure(
        "TFrame",
        background=BG
    )

    # Special frame style used as card panels
    style.configure(
        "Card.TFrame",
        background=CARD
    )

    # ================= Label Style =================
    # Default label style
    style.configure(
        "TLabel",
        background=BG,
        foreground=TEXT,
        font=("Segoe UI", 11)
    )

    # Header label style (used for titles)
    style.configure(
        "Header.TLabel",
        background=BG,
        foreground="#1e3a8a",
        font=("Segoe UI", 22, "bold")
    )

    # ================= Button Style =================
    # Default button appearance
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        background=BUTTON,
        foreground="#1f2937"
    )

    # Button style when mouse is over it
    style.map(
        "TButton",
        background=[
            ("active", "#3b82f6")
        ]
    )

    # ================= Treeview (Table) Style =================
    # Table rows style
    style.configure(
        "Treeview",
        background=WHITE,
        fieldbackground=WHITE,
        foreground=TEXT,
        rowheight=28,
        font=("Segoe UI", 10)
    )

    # Table header style
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#cbd5e1",
        foreground="#334155"
    )
