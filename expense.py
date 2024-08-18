import csv
from datetime import datetime

def load_expenses(file_path):
    """
    Load expenses from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of expense dictionaries.
    """
    expenses = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Validate data before adding it to the list
                if validate_expense(row):
                    expenses.append(row)
                else:
                    print(f"Invalid data found in row: {row}")
        return expenses
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return expenses

def validate_expense(expense):
    """
    Validate an expense entry.

    Args:
        expense (dict): Expense data to validate.

    Returns:
        bool: True if the expense is valid, False otherwise.
    """
    try:
        # Ensure date is present and valid
        date_value = expense.get("Date")
        if not date_value or date_value.strip() == "":
            print("Error: Missing or invalid date.")
            return False
        datetime.strptime(date_value, "%Y-%m-%d")
        
        # Ensure amount is a valid float
        float(expense["Amount"])

        # Add any additional validations as needed (e.g., category validation)
        return True
    except (ValueError, KeyError) as e:
        print(f"Validation error: {e}")
        return False

def add_expense(file_path, date, name, category, amount):
    """
    Add a new expense to the CSV file.

    Args:
        file_path (str): Path to the CSV file.
        date (str): Date of the expense.
        name (str): Name of the expense.
        category (str): Category of the expense.
        amount (float): Amount of the expense.
    """
    new_expense = {
        "Date": date,
        "Expense Name": name,
        "Category": category,
        "Amount": amount
    }

    if validate_expense(new_expense):
        try:
            with open(file_path, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=new_expense.keys())
                writer.writerow(new_expense)
                print("Expense added successfully.")
        except Exception as e:
            print(f"Error: Could not write to file {file_path}. Exception: {e}")
    else:
        print("Error: Invalid expense data. The expense was not added.")

# Example usage
if __name__ == "__main__":
    file_path = 'expense.csv'
    add_expense(file_path, "2023-08-10", "Dinner", "Food", 30.50)
    expenses = load_expenses(file_path)
    print(expenses)
