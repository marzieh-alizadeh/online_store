import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Service layer imports (business logic)
from services.auth_service import AuthService
from services.product_service import ProductService
from services.cart_service import CartService
from services.comment_service import CommentService
from services.order_service import OrderService

# UI helpers
from ui.cart_window import CartWindow
from ui.style import setup_style
from ui.utils import center_window, format_toman

# Try to import PIL for image support
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class StoreWindow:
    # Main store window for normal users

    def __init__(self, login_root, user):
        # Save login window reference and user info
        self.login_root = login_root
        self.user = user
        self.all_products = []

        # Create new window
        self.root = tk.Toplevel()
        self.root.title("Store")

        # Set window size and style
        center_window(self.root, 1350, 680)
        setup_style(self.root)

        # When user closes window → logout
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

        # Build interface and load data
        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Main container
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        # ================= TOP HEADER =================
        top_frame = ttk.Frame(main)
        top_frame.pack(fill="x", pady=(0, 10))

        left_header = ttk.Frame(top_frame)
        left_header.pack(side="left")

        # Welcome label
        ttk.Label(
            left_header,
            text=f"Welcome, {self.user[0]}",
            style="Header.TLabel"
        ).pack(side="left", padx=(0, 20))

        # User balance label
        self.balance_label = ttk.Label(
            left_header,
            text=f"Balance: {format_toman(self.user[2])}",
            font=("Segoe UI", 11, "bold")
        )
        self.balance_label.pack(side="left")

        # Header buttons
        ttk.Button(top_frame, text="My Orders", command=self.show_my_orders).pack(side="right", padx=5)
        ttk.Button(top_frame, text="Logout", command=self.logout).pack(side="right", padx=5)
        ttk.Button(top_frame, text="Add Balance", command=self.add_balance).pack(side="right", padx=5)

        # ================= LEFT SIDE (PRODUCTS) =================
        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=10)

        # ================= RIGHT SIDE (DETAILS) =================
        right = ttk.Frame(main, width=320)
        right.pack(side="right", fill="y", expand=False, padx=10)
        right.pack_propagate(False)

        # ---------- Filter section ----------
        filter_frame = ttk.Frame(left)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_frame, text="Search:").pack(side="left", padx=5)

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=25)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.apply_filters)

        ttk.Label(filter_frame, text="Category:").pack(side="left", padx=5)

        # Category dropdown
        self.category_var = tk.StringVar()
        self.category_box = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly", width=18)
        self.category_box.pack(side="left", padx=5)
        self.category_box.bind("<<ComboboxSelected>>", self.apply_filters)

        ttk.Button(filter_frame, text="Reset", command=self.reset_filters).pack(side="left", padx=5)

        # ---------- Product table ----------
        columns = ("ID", "Name", "Price", "Stock", "Category")
        self.tree = ttk.Treeview(left, columns=columns, show="headings")

        for column in columns:
            self.tree.heading(column, text=column)

        # Set column widths
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=230, anchor="center")
        self.tree.column("Price", width=160, anchor="center")
        self.tree.column("Stock", width=90, anchor="center")
        self.tree.column("Category", width=130, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # When product selected
        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        # ---------- Action buttons ----------
        button_frame = ttk.Frame(left)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add To Cart", command=self.add_to_cart).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View Cart", command=self.open_cart).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Product Details", command=self.open_product_details).pack(side="left", padx=5)

        # ---------- Right panel content ----------
        self.image_label = ttk.Label(right)
        self.image_label.pack(pady=10)

        self.desc = ttk.Label(right, wraplength=270, justify="left")
        self.desc.pack(pady=10)

        # Comments section
        ttk.Label(right, text="Comments").pack()

        comment_frame = ttk.Frame(right)
        comment_frame.pack(pady=5, fill="x")

        scrollbar = ttk.Scrollbar(comment_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Comment list
        self.comment_box = tk.Listbox(
            comment_frame,
            height=7,
            width=38,
            bg="#2b2b3c",
            fg="white",
            selectbackground="#2563eb",
            yscrollcommand=scrollbar.set
        )
        self.comment_box.pack(side="left")
        scrollbar.config(command=self.comment_box.yview)

        # Comment input
        comment_input_frame = ttk.Frame(right)
        comment_input_frame.pack(fill="x", pady=(5, 0))

        self.new_comment = ttk.Entry(comment_input_frame)
        self.new_comment.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ttk.Button(comment_input_frame, text="Add", command=self.add_comment).pack(side="right")

    # ================= PRODUCT DATA =================
    def load_products(self):
        # Get all products from service
        self.all_products = ProductService.get_all_products()
        self.load_categories()
        self.apply_filters()

    def load_categories(self):
        # Extract unique categories
        categories = []
        for product in self.all_products:
            if len(product) > 4 and product[4] not in categories:
                categories.append(product[4])

        categories.sort()
        self.category_box["values"] = ["All"] + categories
        self.category_box.set("All")

    def apply_filters(self, event=None):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_text = self.search_var.get().strip().lower()
        selected_category = self.category_var.get()

        # Insert filtered products
        for product in self.all_products:
            product_id = str(product[0])
            name = str(product[1])
            price = format_toman(self.calculate_price(product[2], product[5]))
            stock = str(product[3])
            category = str(product[4])

            search_match = (
                search_text == "" or
                search_text in product_id.lower() or
                search_text in name.lower() or
                search_text in category.lower()
            )

            category_match = (
                selected_category in ("", "All") or
                category == selected_category
            )

            if search_match and category_match:
                self.tree.insert("", tk.END, values=(product_id, name, price, stock, category))

    def reset_filters(self):
        # Reset search and category
        self.search_var.set("")
        self.category_box.set("All")
        self.apply_filters()

    # ================= USER ACTIONS =================
    def logout(self):
        # Close store window and show login
        self.root.destroy()
        self.login_root.deiconify()

    def get_selected_product(self):
        # Return selected product data
        selected = self.tree.selection()
        if not selected:
            return None

        values = self.tree.item(selected[0], "values")
        product_id = values[0]

        for p in self.all_products:
            if p[0] == product_id:
                return p

        return None

    def add_to_cart(self):
        # Add selected product to cart
        product = self.get_selected_product()
        if not product:
            messagebox.showwarning("Warning", "Select a product first.")
            return

        quantity = simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1)
        if not quantity:
            return

        success, message = CartService.add_to_cart(self.user[0], product, quantity)

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def open_cart(self):
        # Open cart window
        CartWindow(self.root, self.user, self.refresh_balance)

    def refresh_balance(self):
        # Update balance label
        self.balance_label.config(
            text=f"Balance: {format_toman(self.user[2])}"
        )

    def open_product_details(self):
        # Show product details
        product = self.get_selected_product()
        if not product:
            messagebox.showwarning("Warning", "Select a product.")
            return

        messagebox.showinfo(
            "Product Details",
            f"Name: {product[1]}\n\nDescription:\n{product[6]}"
        )

    def show_details(self, event=None):
        # Show product description, comments and image
        product = self.get_selected_product()
        if not product:
            return

        description = product[6] if len(product) > 6 else ""
        self.desc.config(text=description)

        self.load_comments(product[0])
        self.load_image(product[7] if len(product) > 7 else "")

    def load_comments(self, product_id):
        # Load comments for selected product
        self.comment_box.delete(0, tk.END)
        comments = CommentService.get_comments(product_id)

        for comment in comments:
            self.comment_box.insert(tk.END, comment)

    def add_comment(self):
        # Add new comment
        product = self.get_selected_product()
        if not product:
            messagebox.showwarning("Warning", "Select a product.")
            return

        text = self.new_comment.get()

        success, message = CommentService.add_comment(
            product[0],
            self.user[0],
            text
        )

        if success:
            self.new_comment.delete(0, tk.END)
            self.load_comments(product[0])
        else:
            messagebox.showerror("Error", message)

    def add_balance(self):
        # Add money to user balance
        amount = simpledialog.askfloat("Add Balance", "Enter amount:")
        if not amount or amount <= 0:
            return

        new_balance = float(self.user[2]) + amount

        if AuthService.update_user_balance(self.user[0], new_balance):
            self.user[2] = new_balance
            self.refresh_balance()
            messagebox.showinfo("Success", "Balance updated.")

    def show_my_orders(self):
        # Show user's orders in new window
        orders = OrderService.get_user_orders(self.user[0])

        win = tk.Toplevel(self.root)
        win.title("My Orders")
        center_window(win, 600, 400)

        columns = ("Product", "Qty", "Total", "Date")
        tree = ttk.Treeview(win, columns=columns, show="headings")

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=130)

        tree.pack(fill="both", expand=True, padx=15, pady=15)

        for order in orders:
            total = format_toman(order[3])
            tree.insert("", tk.END, values=(order[1], order[2], total, order[4]))

    def calculate_price(self, price, discount):
        # Calculate final price with discount
        try:
            price = float(price)
            discount = float(discount) if discount else 0
        except:
            return str(price)

        if discount <= 0:
            return f"{price:,.0f} Toman"

        new_price = price * (1 - discount / 100)
        return f"{new_price:,.0f} Toman - {discount:.0f}% OFF"

    def load_image(self, path):
        # Load product image if exists
        if not path or not Image:
            self.image_label.config(image="")
            return

        try:
            img = Image.open(path)
            img = img.resize((220, 220))
            photo = ImageTk.PhotoImage(img)

            self.image_label.config(image=photo)
            self.image_label.image = photo
        except:
            self.image_label.config(image="")
