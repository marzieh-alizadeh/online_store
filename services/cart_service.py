class CartService:
    # This class manages the shopping cart for users

    # Dictionary to store cart items for each user
    # Format: {username: [ {product: [...], quantity: int}, ... ]}
    cart_items = {}

    @staticmethod
    def add_to_cart(username, product, quantity):
        # Check if the username is valid
        if not username:
            return False, "Invalid user."

        # Create a new cart for the user if it does not exist
        if username not in CartService.cart_items:
            CartService.cart_items[username] = []

        # Get the user's cart
        user_cart = CartService.cart_items[username]

        try:
            # Convert quantity and stock to integers
            quantity = int(quantity)
            stock = int(product[3])
        except (ValueError, TypeError, IndexError):
            # Return error if conversion fails
            return False, "Invalid quantity or stock."

        # Check if quantity is valid
        if quantity <= 0:
            return False, "Quantity must be greater than zero."

        # Check if enough stock is available
        if quantity > stock:
            return False, "Not enough stock available."

        # Get the product ID
        product_id = product[0]

        # If product already exists in user's cart, increase quantity
        for item in user_cart:
            if item["product"][0] == product_id:
                new_quantity = item["quantity"] + quantity

                # Check again if the new quantity exceeds stock
                if new_quantity > stock:
                    return False, "Not enough stock available."

                # Update the quantity in the cart
                item["quantity"] = new_quantity
                return True, "Product quantity updated in cart."

        # Add new product to the user's cart
        user_cart.append({
            "product": product,
            "quantity": quantity
        })

        return True, "Product added to cart."

    @staticmethod
    def remove_from_cart(username, product_id):
        # Check if username is valid
        if not username:
            return False

        # Check if the user has a cart
        if username not in CartService.cart_items:
            return False

        # Get the user's cart
        user_cart = CartService.cart_items[username]

        # Save the number of items before removing
        before_count = len(user_cart)

        # Remove the selected product from the cart
        CartService.cart_items[username] = [
            item for item in user_cart
            if item["product"][0] != product_id
        ]

        # Return True if an item was removed
        return len(CartService.cart_items[username]) < before_count

    @staticmethod
    def clear_cart(username):
        # Check if username is valid
        if not username:
            return False

        # Clear all items in the user's cart
        if username in CartService.cart_items:
            CartService.cart_items[username].clear()
            return True

        return False

    @staticmethod
    def get_cart_items(username):
        # Check if username is valid
        if not username:
            return []

        # Create an empty cart if the user does not have one
        if username not in CartService.cart_items:
            CartService.cart_items[username] = []

        # Return the user's cart items
        return CartService.cart_items[username]

    @staticmethod
    def get_total(username):
        # Return 0 if username is not valid
        if not username:
            return 0

        # Return 0 if user has no cart
        if username not in CartService.cart_items:
            return 0

        # Get the user's cart
        user_cart = CartService.cart_items[username]

        total = 0

        # Calculate the total price of all items in the cart
        for item in user_cart:
            product = item["product"]
            quantity = item["quantity"]

            try:
                # Get price and discount from product data
                price = float(product[2])
                discount = float(product[5]) if product[5] else 0
            except (ValueError, TypeError, IndexError):
                # Skip invalid product data
                continue

            # Calculate the final price after discount
            final_price = price - (price * discount / 100)

            # Add the price of this product to the total
            total += final_price * quantity

        # Return the total price of the cart
        return total
