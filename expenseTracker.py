import csv
import os
from excel_exporter import exportExpensesToExcel

def getUserExpense():
    print("Getting User Expense!")
    while True:
        try:
            name = input("Enter expense name: ").strip()
            if not name:
                raise ValueError("Expense name cannot be empty.")
            
            amount = float(input("Enter expense amount: ").strip())
            if amount <= 0:
                raise ValueError("Expense amount must be a positive number.")
            
            print("Available categories:")
            categories = ["Food", "Rent", "Utilities", "Transportation", "Entertainment", "Other"]
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")
            
            category_num = int(input("Select a category number: ").strip())
            if category_num not in range(1, len(categories) + 1):
                raise ValueError("Invalid category number selected.")
            
            category = categories[category_num - 1]
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
    
    print(f"Expense added: {name}, {category}, ${amount:.2f}")
    return {"name": name, "category": category, "amount": amount}

def saveExpenseToFile(expense, filePath):
    file_exists = os.path.isfile(filePath)
    with open(filePath, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Expense Name", "Category", "Amount"])
        writer.writerow([expense["name"], expense["category"], expense["amount"]])
    print("Expense saved successfully.")

def summarizeExpenses(filePath, budget):
    print(f"Summarizing expenses from {filePath}...")

    totalSpent = 0
    expenses = []

    try:
        with open(filePath, "r") as file:
            reader = csv.DictReader(file)
            if 'Amount' not in reader.fieldnames:
                raise ValueError("CSV file is missing the 'Amount' column.")
            
            for row in reader:
                amount = float(row["Amount"])
                totalSpent += amount
                expenses.append(row)
    except FileNotFoundError:
        print("No expenses found. Start by adding your first expense.")
        return []
    except ValueError as ve:
        print(f"Error reading expenses: {ve}")
        return []
    except Exception as e:
        print(f"Unexpected error reading expenses: {e}")
        return []

    print(f"Total Spent: ${totalSpent:.2f}")
    print(f"Budget: ${budget:.2f}")
    print(f"Remaining: ${budget - totalSpent:.2f}")

    return expenses

def main():
    print(f"Running Expense Tracker!")
    expenseFilePath = "expense.csv"
    budget = 2000  # Placeholder budget, could be replaced with user input

    expense = getUserExpense()
    saveExpenseToFile(expense, expenseFilePath)
    summarizeExpenses(expenseFilePath, budget)
    exportExpensesToExcel(expenseFilePath, budget)

if __name__ == "__main__":
    main()
