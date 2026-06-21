import hashlib
from services.file_manager import FileManager

# Path of the user data file
USER_FILE = "data/users.csv"

# Header used when creating the user file
USER_HEADER = ["username", "password", "balance", "role"]


class AuthService:
    # This class handles user authentication and user management

    @staticmethod
    def register(username, password):
        # Ensure the user file exists, if not create it with header
        FileManager.ensure_file(USER_FILE, USER_HEADER)

        # Remove extra spaces from username
        username = username.strip()

        # Check minimum username length
        if len(username) < 3:
            return False, "Username must be at least 3 characters."

        # Check minimum password length
        if len(password) < 4:
            return False, "Password must be at least 4 characters."

        # Hash the password using SHA256 for security
        password = hashlib.sha256(password.encode()).hexdigest()

        # Read all users from the file
        users = FileManager.read_file(USER_FILE)

        # Check if the username already exists
        for user in users[1:]:
            if len(user) > 0 and user[0] == username:
                return False, "User already exists."

        # Create a new user with default balance 0 and role Customer
        new_user = [username, password, "0", "Customer"]

        # Save the new user to the file
        FileManager.append_row(USER_FILE, new_user)

        # Return success message
        return True, "Registration successful."

    @staticmethod
    def login(username, password):
        # Ensure the user file exists
        FileManager.ensure_file(USER_FILE, USER_HEADER)

        # Remove extra spaces from username
        username = username.strip()

        # Hash the entered password for comparison
        password = hashlib.sha256(password.encode()).hexdigest()

        # Read all users from the file
        users = FileManager.read_file(USER_FILE)

        # Search for a user with matching username and password
        for user in users[1:]:
            if len(user) >= 4 and user[0] == username and user[1] == password:
                return user

        # Return None if login fails
        return None

    @staticmethod
    def get_all_users():
        # Ensure the user file exists
        FileManager.ensure_file(USER_FILE, USER_HEADER)

        # Read all users from the file
        users = FileManager.read_file(USER_FILE)

        # If there are no users except header return empty list
        if len(users) <= 1:
            return []

        # Return all users except the header
        return users[1:]

    @staticmethod
    def update_user_balance(username, new_balance):
        # Ensure the user file exists
        FileManager.ensure_file(USER_FILE, USER_HEADER)

        # Read all users from the file
        users = FileManager.read_file(USER_FILE)

        # If file is empty return False
        if len(users) == 0:
            return False

        # Separate header and user data
        header = users[0]
        data = users[1:]

        # Find the user and update their balance
        for user in data:
            if len(user) >= 4 and user[0] == username:
                # Update balance and round to 2 decimal places
                user[2] = str(round(float(new_balance), 2))

                # Save updated data back to the file
                FileManager.write_file(USER_FILE, data, header)

                return True

        # Return False if user was not found
        return False
