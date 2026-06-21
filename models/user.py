class User:
    # This class is used to store basic user information

    def __init__(self, username, password, balance, role):
        # Store the username of the user
        self.username = username

        # Store the user password
        self.password = password

        # Store the user account balance as a float number
        self.balance = float(balance)

        # Store the role of the user (Customer or Admin)
        self.role = role

    def to_list(self):
        # Convert user object data to a list
        # This format is useful for saving user data in a CSV file
        return [
            self.username,
            self.password,
            str(self.balance),
            self.role
        ]


class Customer(User):
    # This class represents a customer user
    # It inherits all properties from the User class

    def __init__(self, username, password, balance=0):
        # Call the parent (User) constructor and set role to "Customer"
        super().__init__(username, password, balance, "Customer")


class Admin(User):
    # This class represents an admin user
    # It inherits all properties from the User class

    def __init__(self, username, password, balance=0):
        # Call the parent (User) constructor and set role to "Admin"
        super().__init__(username, password, balance, "Admin")
