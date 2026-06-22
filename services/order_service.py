from datetime import date
from services.file_manager import FileManager
from services.product_service import ProductService, PRODUCT_HEADER
from services.auth_service import AuthService
from services.cart_service import CartService
from ui.utils import format_toman

# Path of the orders data file
ORDER_FILE = "data/orders.csv"

# Header used when creating the orders file
ORDER_HEADER = [
    "username",
    "product_id",
    "quantity",
    "total",
    "date"
]

# Path of the products data file
PRODUCT_FILE = "data/products.csv"


class OrderService:
    # This class manages order processing and order history

    @staticmethod
    def checkout(username, cart_items):
        # Ensure the order file exists
        FileManager.ensure_file(ORDER_FILE, ORDER_HEADER)

        # Check if username is valid
        if not username:
            return False, "Invalid user."

        # Check if the cart is empty
        if len(cart_items) == 0:
            return False, "Cart is empty."

        # Get all products and users from files
        products = ProductService.get_all_products()
        users = AuthService.get_all_users()

        current_user = None

        # Find the current user in the user list
        for user in users:
            if len(user) >= 4 and user[0] == username:
                current_user = user
                break

        # Return error if user is not found
        if current_user is None:
            return False, "User not found."

        try:
            # Get the user's balance
            user_balance = float(current_user[2])
        except (ValueError, TypeError):
            return False, "Invalid user balance."

        total_price = 0

        # Get today's date
        today = date.today().isoformat()

        # Validate all cart items before completing the order
        for cart_item in cart_items:

            # Check if the cart item structure is valid
            if not isinstance(cart_item, dict):
                return False, "Invalid cart item."

            if "product" not in cart_item or "quantity" not in cart_item:
                return False, "Invalid cart item structure."

            product = cart_item["product"]

            try:
                # Convert quantity to integer
                quantity = int(cart_item["quantity"])
            except (ValueError, TypeError):
                return False, "Invalid quantity."

            # Quantity must be greater than zero
            if quantity <= 0:
                return False, "Quantity must be greater than zero."

            # Check if product data is valid
            if product is None or len(product) < 6:
                return False, "Invalid product in cart."

            product_id = product[0]

            current_product = None

            # Find the product in the product list
            for p in products:
                if len(p) >= 6 and p[0] == product_id:
                    current_product = p
                    break

            # Return error if product does not exist
            if current_product is None:
                return False, f"Product {product_id} not found."

            # Calculate the final price using ProductService
            final_price = ProductService.calculate_final_price(current_product)

            # Calculate total price for this item
            item_total = round(final_price * quantity, 2)

            total_price += item_total

            # Check if user balance is enough
            if total_price > user_balance:
                return False, "Not enough balance."

            # Create a new order record
            order = [
                username,
                product_id,
                str(quantity),
                str(item_total),
                today
            ]

            # Save the order to the file
            FileManager.append_row(ORDER_FILE, order)

            # Reduce the product stock after purchase
            current_product[3] = str(int(current_product[3]) - quantity)

        # Update the products file after all items are processed
        FileManager.write_file(PRODUCT_FILE, products, PRODUCT_HEADER)

        # Update the user's balance after purchase
        new_balance = user_balance - total_price
        AuthService.update_user_balance(username, new_balance)

        # Clear the user's cart after checkout
        CartService.clear_cart(username)

        # Return success message with total price
        return True, f"Order completed successfully. Total price: {format_toman(total_price)}"


    @staticmethod
    def get_all_orders():
        # Ensure the order file exists
        FileManager.ensure_file(ORDER_FILE, ORDER_HEADER)

        # Read all orders from the file
        orders = FileManager.read_file(ORDER_FILE)

        # If there are no orders except header return empty list
        if len(orders) <= 1:
            return []

        # Return all orders except the header
        return orders[1:]


    @staticmethod
    def get_user_orders(username):
        # Get all orders
        orders = OrderService.get_all_orders()

        result = []

        # Filter orders that belong to the specified user
        for order in orders:
            if len(order) >= 5 and order[0] == username:
                result.append(order)

        return result


    @staticmethod
    def get_total_sales():
        # Get all orders
        orders = OrderService.get_all_orders()

        total = 0

        # Calculate total sales from all orders
        for order in orders:
            if len(order) >= 4:
                total += float(order[3])

        return format_toman(round(total, 2))


    @staticmethod
    def get_product_sales(product_id):
        # Get all orders
        orders = OrderService.get_all_orders()

        total = 0

        # Calculate total sales for a specific product
        for order in orders:
            if len(order) >= 4 and order[1] == product_id:
                total += float(order[3])

        return format_toman(round(total, 2))
