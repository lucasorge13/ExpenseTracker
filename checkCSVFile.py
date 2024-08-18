import csv
import os
import logging

# Set up logging
logging.basicConfig(filename='checkCSVFile.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validate_csv_file(file_path):
    """
    Validate the structure and content of the CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    required_columns = ["Date", "Expense Name", "Category", "Amount"]

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        print("Error: File not found.")
        return False

    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames

            # Check for missing columns
            missing_columns = [col for col in required_columns if col not in headers]
            if missing_columns:
                logging.error(f"Missing columns: {missing_columns}")
                print(f"Error: Missing columns: {missing_columns}")
                return False

            # Validate data types
            for row in reader:
                try:
                    float(row["Amount"])
                except ValueError:
                    logging.error(f"Invalid amount found: {row['Amount']} in row {reader.line_num}")
                    print(f"Error: Invalid amount found in row {reader.line_num}.")
                    return False

                # Additional validations can be added here (e.g., date format, category validation)

        logging.info("CSV file validated successfully.")
        print("CSV file validated successfully.")
        return True

    except Exception as e:
        logging.exception(f"Failed to validate CSV file: {str(e)}")
        print(f"Error: Failed to validate CSV file: {str(e)}")
        return False


# Example usage
if __name__ == "__main__":
    file_path = 'expense.csv'  # Replace with your actual file path
    validate_csv_file(file_path)
