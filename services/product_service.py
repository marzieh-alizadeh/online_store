from services.file_manager import FileManager
from ui.utils import format_toman

# Path of the products data file
PRODUCT_FILE = "data/products.csv"

# Header used when creating the products file
PRODUCT_HEADER = [
    "product_id",
    "name",
    "price",
    "stock",
    "category",
    "discount",
    "description",
    "image_path"
]


class ProductService:
    # This class manages product operations such as add, update, delete and retrieval

    @staticmethod
    def validate_product(product_id, name, price, stock, category, discount):
        # Remove extra spaces from inputs
        product_id = product_id.strip()
        name = name.strip()
        category = category.strip()

        # Check required fields
        if product_id == "" or name == "" or category == "":
            return False, "ID, name and category are required."

        try:
            # Convert values to correct types
            price = float(price)
            stock = int(stock)
            discount = float(discount)
        except ValueError:
            return False, "Price, stock and discount must be valid numbers."

        # Validate price
        if price < 0:
            return False, "Price cannot be negative."

        # Validate stock
        if stock < 0:
            return False, "Stock cannot be negative."

        # Validate discount range
        if discount < 0 or discount > 100:
            return False, "Discount must be between 0 and 100."

        return True, "Valid product."

    @staticmethod
    def add_product(product_id, name, price, stock, category, discount, description, image):
        # Ensure the product file exists
        FileManager.ensure_file(PRODUCT_FILE, PRODUCT_HEADER)

        # Validate product information
        valid, message = ProductService.validate_product(
            product_id,
            name,
            price,
            stock,
            category,
            discount
        )

        if not valid:
            return False, message

        # Read all products from the file
        products = FileManager.read_file(PRODUCT_FILE)

        # Check if the product already exists
        for product in products[1:]:
            if len(product) > 0 and product[0] == product_id:
                return False, "Product already exists."

        # Create a new product row
        row = [
            product_id.strip(),
            name.strip(),
            str(float(price)),
            str(int(stock)),
            category.strip(),
            str(float(discount)),
            description.strip(),
            image.strip()
        ]

        # Save the new product to the file
        FileManager.append_row(PRODUCT_FILE, row)

        return True, "Product added successfully."

    @staticmethod
    def delete_product(product_id):
        # Ensure the product file exists
        FileManager.ensure_file(PRODUCT_FILE, PRODUCT_HEADER)

        # Read all products
        products = FileManager.read_file(PRODUCT_FILE)

        # Check if there are any products
        if len(products) <= 1:
            return False, "No products available."

        header = products[0]
        data = products[1:]
        new_data = []
        deleted = False

        # Search for the product and remove it
        for product in data:
            if len(product) > 0 and product[0] == product_id:
                deleted = True
            else:
                new_data.append(product)

        # If product was not found
        if not deleted:
            return False, "Product not found."

        # Save the updated product list
        FileManager.write_file(PRODUCT_FILE, new_data, header)

        return True, "Product deleted successfully."

    @staticmethod
    def update_product(product_id, name, price, stock, category, discount, description, image):
        # Ensure the product file exists
        FileManager.ensure_file(PRODUCT_FILE, PRODUCT_HEADER)

        # Validate product information
        valid, message = ProductService.validate_product(
            product_id,
            name,
            price,
            stock,
            category,
            discount
        )

        if not valid:
            return False, message

        # Read all products
        products = FileManager.read_file(PRODUCT_FILE)

        # Check if product list is empty
        if len(products) <= 1:
            return False, "No products available."

        header = products[0]
        data = products[1:]
        updated = False

        # Find the product and update its information
        for product in data:
            if len(product) > 0 and product[0] == product_id:
                product[1] = name.strip()
                product[2] = str(float(price))
                product[3] = str(int(stock))
                product[4] = category.strip()
                product[5] = str(float(discount))
                product[6] = description.strip()
                product[7] = image.strip()
                updated = True

        # If product was not found
        if not updated:
            return False, "Product not found."

        # Save updated product data
        FileManager.write_file(PRODUCT_FILE, data, header)

        return True, "Product updated successfully."

    @staticmethod
    def get_all_products():
        # Ensure the product file exists
        FileManager.ensure_file(PRODUCT_FILE, PRODUCT_HEADER)

        # Read all products
        products = FileManager.read_file(PRODUCT_FILE)

        # Return empty list if there are no products
        if len(products) <= 1:
            return []

        result = []

        # Process each product row
        for product in products[1:]:

            # Skip empty rows
            if not product or len(product) == 0:
                continue

            # Fix incomplete product rows
            product = ProductService.fix_product_row(product)

            # Skip rows without product ID
            if product[0].strip() == "":
                continue

            result.append(product)

        return result


    @staticmethod
    def fix_product_row(product):
        # Ensure the product row has exactly 8 columns
        while len(product) < 8:
            product.append("")

        # Set discount to 0 if it is empty
        if len(product) > 5 and product[5] == "":
            product[5] = "0"

        return product


    @staticmethod
    def get_product_by_id(product_id):
        # Get all products
        products = ProductService.get_all_products()

        # Search for the product by ID
        for product in products:
            if len(product) > 0 and product[0] == product_id:
                return product

        # Return None if product is not found
        return None


    @staticmethod
    def calculate_final_price(product):
        # Get product price
        price = float(product[2])

        # Get product discount
        discount = float(product[5]) if len(product) > 5 and product[5] != "" else 0

        # Calculate final price after discount
        return price * (1 - discount / 100)

    @staticmethod
    def get_formatted_price(product):
        """Returns the base price formatted with Toman."""
        try:
            price = float(product.price) if not isinstance(product.price, float) else product.price
            return format_toman(price)
        except (ValueError, TypeError):
            return format_toman(product.price)

    @staticmethod
    def get_formatted_final_price(product):
        """Returns the final price (after discount) formatted with Toman."""
        final_price = ProductService.calculate_final_price(product)
        return format_toman(final_price)

    @staticmethod
    def get_formatted_price_with_discount(product):
        """Returns a tuple of (formatted_final_price, discount_display_string)
        Useful for Treeview display."""
        final_price = ProductService.calculate_final_price(product)
        final_price_str = format_toman(final_price)
        try:
            discount_float = float(product.discount)
            if discount_float > 0:
                discount_str = f"{int(discount_float)}% off"
            else:
                discount_str = "No"
        except (ValueError, TypeError):
            discount_str = "N/A"
        return final_price_str, discount_str
