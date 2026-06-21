import tkinter as tk
from tkinter import ttk, messagebox

from ui.utils import format_toman
from services.cart_service import CartService
from services.order_service import OrderService


class CartWindow:
    # This class manages the shopping cart window for the user

    def __init__(self, parent, user, refresh_callback=None):
        # Save parent window, user data, and refresh function
        self.parent = parent
        self.user = user
        self.refresh_callback = refresh_callback

        # Create cart window
        self.window = tk.Toplevel(parent)
        self.window.title("View Cart")

        # Configure window size
        self.window.geometry("950x600")
        self.window.minsize(900, 500)
        self.window.resizable(True, True)

        # Build UI and load cart data
        self.build_ui()
        self.load_cart()

    def build_ui(self):
        # Main container frame
        main_frame = ttk.Frame(self.window, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Window title
        ttk.Label(main_frame, text="Your Cart", style="Header.TLabel").pack(pady=(0, 10))

        # Frame for cart table
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True)

        # Table columns
        columns = ("id", "name", "price", "discount", "quantity", "subtotal")

        # Create cart table
        self.cart_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        # Set column titles
        self.cart_table.heading("id", text="ID")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("discount", text="Discount")
        self.cart_table.heading("quantity", text="Quantity")
        self.cart_table.heading("subtotal", text="Subtotal")

        # Display table
        self.cart_table.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.cart_table.yview)
        scrollbar.pack(side="right", fill="y")

        self.cart_table.configure(yscrollcommand=scrollbar.set)

        # Bottom section for total and buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=(15, 0))

        # Label to show total price
        self.total_label = ttk.Label(bottom_frame, text="Total: 0", font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=(0, 10))

        # Buttons frame
        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack()

        # Cart action buttons
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear Cart", command=self.clear_cart).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Checkout", command=self.checkout).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).grid(row=0, column=3, padx=5)

    def load_cart(self):
        # Clear existing rows in the cart table
        for row in self.cart_table.get_children():
            self.cart_table.delete(row)

        # Get username
        username = self.user[0]

        # Get cart items for the user
        cart_items = CartService.get_cart_items(username)

        # Insert each cart item into the table
        for item in cart_items:
            product = item["product"]
            quantity = item["quantity"]

            product_id = product[0]
            name = product[1]

            # Get price and discount
            price = float(product[2])
            discount = float(product[5]) if product[5] else 0

            # Calculate final price after discount
            final_price = price - (price * discount / 100)

            # Calculate subtotal for this product
            subtotal = final_price * quantity

            # Insert row into the table
            self.cart_table.insert(
                "",
                "end",
                values=(
                    product_id,
                    name,
                    format_toman(price),
                    f"{discount:.0f}%",
                    quantity,
                    format_toman(subtotal)
                )
            )

        # Calculate total price of the cart
        total = CartService.get_total(username)

        # Update total label
        self.total_label.config(text=f"Total: {format_toman(total)}")

    def remove_selected(self):
        # Get selected row from table
        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a product to remove.")
            return

        # Get selected product ID
        values = self.cart_table.item(selected[0], "values")
        product_id = values[0]

        username = self.user[0]

        # Remove product from cart
        removed = CartService.remove_from_cart(username, product_id)

        if removed:
            messagebox.showinfo("Success", "Product removed from cart.")
            self.load_cart()
        else:
            messagebox.showerror("Error", "Product could not be removed.")

    def clear_cart(self):
        # Get username
        username = self.user[0]

        # Check if cart is already empty
        if not CartService.get_cart_items(username):
            messagebox.showwarning("Warning", "Cart is already empty.")
            return

        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear your cart?")

        if confirm:
            # Clear cart items
            CartService.clear_cart(username)

            # Reload cart table
            self.load_cart()

    def checkout(self):
        # Get username and cart items
        username = self.user[0]
        cart_items = CartService.get_cart_items(username)

        # Prevent checkout if cart is empty
        if not cart_items:
            messagebox.showwarning("Warning", "Your cart is empty.")
            return

        # Calculate total before checkout
        total_before = CartService.get_total(username)

        # Process checkout using OrderService
        success, message = OrderService.checkout(username, cart_items)

        if success:
            # Show success message
            messagebox.showinfo("Success", message)

            # Update user's balance locally
            self.user[2] = float(self.user[2]) - total_before

            # Reload cart
            self.load_cart()

            # Refresh parent window if needed
            if self.refresh_callback:
                self.refresh_callback()

        else:
            # Show error message if checkout failed
            messagebox.showerror("Error", message)
