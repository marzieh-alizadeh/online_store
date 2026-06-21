# ================= Window Position Helper =================
# This function places a window in the center of the screen
def center_window(win, w=900, h=500):

    # Update window tasks to ensure correct size calculations
    win.update_idletasks()

    # Get the width of the user's screen
    screen_width = win.winfo_screenwidth()

    # Get the height of the user's screen
    screen_height = win.winfo_screenheight()

    # Calculate the horizontal position for centering the window
    x = int((screen_width / 2) - (w / 2))

    # Calculate the vertical position for centering the window
    y = int((screen_height / 2) - (h / 2))

    # Apply the window size and position
    # Format: width x height + x_position + y_position
    win.geometry(f"{w}x{h}+{x}+{y}")


# ================= Currency Formatter =================
# This function formats numbers into Toman currency style
def format_toman(amount):
    """
    Convert numbers to Toman format with Persian thousands separator.

    Example:
    250000  ->  250.000 تومان
    """

    # Try converting the input to float
    try:
        amount = float(amount)

    # If conversion fails (not a number), return the original value
    except (ValueError, TypeError):
        return str(amount)

    # Format number with thousands separator
    # Python normally uses commas: 250,000
    # We replace commas with dots to match Persian style
    return f"{amount:,.0f}".replace(",", ".") + " تومان"
