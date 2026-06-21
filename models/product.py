class Product:
    # This class is used to store product information

    def __init__(
        self,
        product_id,
        name,
        price,
        stock,
        category,
        discount=0,
        description="",
        image_path=""
    ):
        # Store the product ID
        self.product_id = product_id

        # Store the product name
        self.name = name

        # Store the product price as a float number
        self.price = float(price)

        # Store the number of available products as an integer
        self.stock = int(stock)

        # Store the product category
        self.category = category

        # Store the discount percentage
        self.discount = float(discount)

        # Store a short description of the product
        self.description = description

        # Store the image path of the product
        self.image_path = image_path

    def get_final_price(self):
        # Calculate and return the final price after applying discount
        return self.price * (1 - self.discount / 100)

    def to_list(self):
        # Convert product object data to a list
        # This format is useful for saving product data in a CSV file
        return [
            self.product_id,
            self.name,
            str(self.price),
            str(self.stock),
            self.category,
            str(self.discount),
            self.description,
            self.image_path
        ]
