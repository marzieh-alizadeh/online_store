import csv
import os


class FileManager:
    # This class handles reading and writing CSV files used in the system

    @staticmethod
    def ensure_file(file_path, header):
        # Get the folder path from the file path
        folder = os.path.dirname(file_path)

        # Create the folder if it does not exist
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        # Create the file with header if it does not exist or is empty
        if not os.path.exists(file_path):
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Write the header row to the file
                writer.writerow(header)

    @staticmethod
    def read_file(file_path):
        # Return an empty list if the file does not exist
        if not os.path.exists(file_path):
            return []

        data = []

        # Open the CSV file for reading
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            # Read each row and store it in the list
            for row in reader:
                if row:
                    data.append(row)

        # Return all rows from the file
        return data

    @staticmethod
    def write_file(file_path, data, header):
        # Get the folder path from the file path
        folder = os.path.dirname(file_path)

        # Create the folder if it does not exist
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        # Open the file in write mode
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write the header first
            writer.writerow(header)

            # Write all data rows
            for row in data:
                writer.writerow(row)

    @staticmethod
    def append_row(file_path, row):
        # Get the folder path from the file path
        folder = os.path.dirname(file_path)

        # Create the folder if it does not exist
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        # Open the file in append mode to add a new row
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Add the new row to the end of the file
            writer.writerow(row)
