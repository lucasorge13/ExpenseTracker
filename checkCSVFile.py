import csv
import os

def check_and_fix_csv(filePath):
    required_headers = ["Expense Name", "Category", "Amount"]
    
    # Check if the file exists
    if not os.path.exists(filePath):
        print(f"{filePath} does not exist. A new file will be created.")
        with open(filePath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(required_headers)
        return

    # Read the existing headers
    with open(filePath, "r") as file:
        reader = csv.reader(file)
        headers = next(reader, None)
        
        if headers != required_headers:
            print("CSV file headers are incorrect or missing. Fixing headers...")
            data = list(reader)  # Read the rest of the data

            # Recreate the file with correct headers
            with open(filePath, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(required_headers)
                writer.writerows(data)  # Write the existing data back into the file
        else:
            print("CSV file headers are correct.")

# Run the check on your CSV file
expenseFilePath = "expense.csv"
check_and_fix_csv(expenseFilePath)
