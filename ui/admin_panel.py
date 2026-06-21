import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from services.product_service import ProductService
from services.order_service import OrderService
from ui.style import setup_style
from ui.utils import center_window, format_toman


class AdminPanel:
    # This class manages the admin interface for product and order management

    def __init__(self, login_root, user):
        # Save login window and current admin user
        self.login_root = login_root
        self.user = user

        # Create admin panel window
        self.root = tk.Toplevel()
        self.root.title("Admin Panel")

        # Center window and apply style
        center_window(self.root, 900, 600)
        setup_style(self.root)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

        # Build interface and load products
        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Main container frame
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        # Top section (title and logout)
        top = ttk.Frame(main)
        top.pack(fill="x", pady=(0, 10))

        ttk.Label(
            top,
            text="Admin Panel",
            style="Header.TLabel"
        ).pack(side="left")

        ttk.Button(
            top,
            text="Logout",
            command=self.logout
        ).pack(side="right", padx=5)

        # Table columns for product list
        columns = ("ID", "Name", "Price", "Stock", "Category", "Discount")

        # Product table
        self.tree = ttk.Treeview(
            main,
            columns=columns,
            show="headings"
        )

        # Configure table columns
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center", width=120)

        self.tree.pack(fill="both", expand=True, pady=10)

        # Button section
        button_frame = ttk.Frame(main)
        button_frame.pack(pady=10)

        # Product management buttons
        ttk.Button(
            button_frame,
            text="Add Product",
            command=self.add_product_window
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Edit Product",
            command=self.edit_product_window
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Delete Product",
            command=self.delete_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.load_products
        ).pack(side="left", padx=5)

        # Order and sales buttons
        ttk.Button(
            button_frame,
            text="View Orders",
            command=self.view_orders
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Sales Report",
            command=self.sales_report
        ).pack(side="left", padx=5)

    def load_products(self):
        # Remove existing rows from the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get all products from the service
        products = ProductService.get_all_products()

        # Insert products into the table
        for product in products:
            self.tree.insert(
                "",
                tk.END,
                iid=product[0],              # product_id (list index 0)
                values=(
                        product[0],              # ID
                        product[1],              # Name
                        format_toman(product[2]), # Price (formatted with Toman)
                        product[3],              # Stock
                        product[4],              # Category
                        product[5]               # Discount 
                ))
    def get_selected_product_id(self):
        # Get the selected item from the table
        selected = self.tree.selection()

        # Show warning if nothing is selected
        if not selected:
            messagebox.showwarning("Warning", "Please select a product.")
            return None

        # Get selected row data
        item = self.tree.item(selected[0])

        # Return the product ID
        return item["values"][0]

    def add_product_window(self):
        # Open the product form for adding a new product
        self.product_form_window("Add Product")

    def edit_product_window(self):
        # Get selected product ID
        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        # Get product data
        product = ProductService.get_product_by_id(product_id)

        if product is None:
            messagebox.showerror("Error", "Product not found.")
            return

        # Open form with product data
        self.product_form_window("Edit Product", product)

    def product_form_window(self, title, product=None):
        # Create product form window
        win = tk.Toplevel(self.root)
        win.title(title)

        center_window(win, 430, 500)

        entries = {}

        # Product fields
        fields = [
            "ID",
            "Name",
            "Price",
            "Stock",
            "Category",
            "Discount",
            "Description",
            "Image"
        ]

        # Create input fields
        for index, field in enumerate(fields):
            ttk.Label(
                win,
                text=field
            ).grid(row=index, column=0, pady=5, padx=8, sticky="w")

            entry = ttk.Entry(win, width=35)
            entry.grid(row=index, column=1, pady=5, padx=8)

            entries[field] = entry

        # If editing, fill fields with existing product data
        if product is not None:
            entries["ID"].insert(0, product[0])
            entries["ID"].config(state="disabled")
            entries["Name"].insert(0, product[1])
            entries["Price"].insert(0, product[2])
            entries["Stock"].insert(0, product[3])
            entries["Category"].insert(0, product[4])
            entries["Discount"].insert(0, product[5])
            entries["Description"].insert(0, product[6])
            entries["Image"].insert(0, product[7])

        def choose_image():
            # Open file dialog to select an image
            path = filedialog.askopenfilename(
                title="Choose Image",
                filetypes=[
                    ("Image Files", "*.png *.jpg *.jpeg *.gif"),
                    ("All Files", "*.*")
                ]
            )

            if path:
                entries["Image"].delete(0, tk.END)
                entries["Image"].insert(0, path)

        # Button for selecting image
        ttk.Button(
            win,
            text="Choose Image",
            command=choose_image
        ).grid(row=len(fields), column=0, columnspan=2, pady=5)

        def save():
            # Get product ID depending on add or edit
            product_id = product[0] if product is not None else entries["ID"].get()

            # Add new product
            if product is None:
                success, message = ProductService.add_product(
                    product_id,
                    entries["Name"].get(),
                    entries["Price"].get(),
                    entries["Stock"].get(),
                    entries["Category"].get(),
                    entries["Discount"].get(),
                    entries["Description"].get(),
                    entries["Image"].get()
                )
            else:
                # Update existing product
                success, message = ProductService.update_product(
                    product_id,
                    entries["Name"].get(),
                    entries["Price"].get(),
                    entries["Stock"].get(),
                    entries["Category"].get(),
                    entries["Discount"].get(),
                    entries["Description"].get(),
                    entries["Image"].get()
                )

            # Show result message
            if success:
                messagebox.showinfo("Success", message)
                win.destroy()
                self.load_products()
            else:
                messagebox.showerror("Error", message)

        # Save button
        ttk.Button(
            win,
            text="Save",
            command=save
        ).grid(row=len(fields) + 1, column=0, columnspan=2, pady=15)

    def delete_product(self):
        # Get selected product ID
        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if not confirm:
            return

        # Delete the product
        success, message = ProductService.delete_product(product_id)

        if success:
            messagebox.showinfo("Success", message)
            self.load_products()
        else:
            messagebox.showerror("Error", message)

    def view_orders(self):
        # Get all orders
        orders = OrderService.get_all_orders()

        # Create orders window
        win = tk.Toplevel(self.root)
        win.title("Orders")

        center_window(win, 750, 450)

        columns = ("Username", "Product", "Qty", "Total", "Date")

        # Orders table
        tree = ttk.Treeview(
            win,
            columns=columns,
            show="headings"
        )

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=130)

        tree.pack(fill="both", expand=True, padx=15, pady=15)

        # Insert order rows
        for order in orders:
            tree.insert("", tk.END, values=(
                order[0],              # Username
                order[1],              # Product
                order[2],              # Qty
                format_toman(order[3]),  # Total
                order[4]               # Date
            ))

    def sales_report(self):
        # Get sales data
        total_sales = OrderService.get_total_sales()
        orders = OrderService.get_all_orders()
        products = ProductService.get_all_products()

        order_count = len(orders)

        # Create sales report window
        win = tk.Toplevel(self.root)
        win.title("Sales Report")

        center_window(win, 650, 500)

        main = ttk.Frame(win, padding=15)
        main.pack(fill="both", expand=True)

        # Report title
        ttk.Label(
            main,
            text="Sales Report",
            style="Header.TLabel"
        ).pack(pady=(0, 10))

        # Summary section
        summary_frame = ttk.Frame(main)
        summary_frame.pack(fill="x", pady=10)

        ttk.Label(
            summary_frame,
            text=f"Total Orders: {order_count}",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=3)

        ttk.Label(
            summary_frame,
            text=f"Total Sales: {format_toman(total_sales)}",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=3)

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=10)

        # Sales by product title
        ttk.Label(
            main,
            text="Sales By Product",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(5, 10))

        columns = ("Product ID", "Product Name", "Sales")

        # Sales table
        sales_tree = ttk.Treeview(
            main,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:
            sales_tree.heading(column, text=column)
            sales_tree.column(column, anchor="center", width=180)

        sales_tree.pack(fill="both", expand=True, pady=5)

        # Insert sales data for each product
        for product in products:
            product_id = product[0]
            product_name = product[1]

            product_sales = OrderService.get_product_sales(product_id)

            sales_tree.insert(
                "",
                tk.END,
                values=(
                    product_id,
                    product_name,
                    format_toman(product_sales)
                )
            )

        # Close button
        ttk.Button(
            main,
            text="Close",
            command=win.destroy
        ).pack(pady=10)

    def logout(self):
        # Close admin panel and return to login window
        self.root.destroy()
        self.login_root.deiconify()
