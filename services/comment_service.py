from datetime import date
from services.file_manager import FileManager


# Path of the comments data file
COMMENT_FILE = "data/comments.csv"

# Header used when creating the comments file
COMMENT_HEADER = [
    "username",
    "product_id",
    "text",
    "date"
]


class CommentService:
    # This class manages product comments

    @staticmethod
    def add_comment(product_id, username, text):
        # Ensure the comment file exists, if not create it with header
        FileManager.ensure_file(COMMENT_FILE, COMMENT_HEADER)

        # Remove extra spaces from the comment text
        text = text.strip()

        # Check if comment is empty
        if text == "":
            return False, "Comment cannot be empty."

        # Get today's date in ISO format (YYYY-MM-DD)
        today = date.today().isoformat()

        # Create a row to store the comment
        row = [
            str(username).strip(),
            str(product_id).strip(),
            text,
            today
        ]

        # Save the comment to the file
        FileManager.append_row(COMMENT_FILE, row)

        return True, "Comment added successfully."

    @staticmethod
    def get_comments(product_id):
        # Ensure the comment file exists
        FileManager.ensure_file(COMMENT_FILE, COMMENT_HEADER)

        # Convert product_id to string and remove extra spaces
        product_id = str(product_id).strip()

        # Read all comments from the file
        comments = FileManager.read_file(COMMENT_FILE)

        # If there are no comments except header return empty list
        if len(comments) <= 1:
            return []

        result = []

        # Search for comments related to the selected product
        for comment in comments[1:]:
            if len(comment) >= 4 and str(comment[1]).strip() == product_id:
                # Format the comment for display
                result.append(f"{comment[0]} ({comment[3]}): {comment[2]}")

        # Return the list of comments for the product
        return result
