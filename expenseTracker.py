from expense import Expense
import csv
import os
from excel_exporter import exportExpensesToExcel

def getUserExpense():
    print(f"Getting User Expense!")

    expenseName = input("Enter expense name: ")
    expenseAmount = float(input("Enter expense amount: "))

    expenseCategories = [
        "Food", 
        "Rent", 
        "Utilities", 
        "Transportation", 
        "Entertainment", 
        "Other"
    ]

    print("Available categories:")
    for index, category in enumerate(expenseCategories, start=1):
        print(f"{index}. {category}")
    
    categoryIndex = int(input("Select a category number: ")) - 1
    expenseCategory = expenseCategories[categoryIndex]

    return Expense(expenseName, expenseCategory, expenseAmount)

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
            for row in reader:
                amount = float(row["Amount"])
                totalSpent += amount
                expenses.append(row)
    except FileNotFoundError:
        print("No expenses found. Start by adding your first expense.")
        return []
    except Exception as e:
        print(f"Error reading expenses: {e}")
        return []

    print(f"Total Spent: ${totalSpent:.2f}")
    print(f"Budget: ${budget:.2f}")
    print(f"Remaining: ${budget - totalSpent:.2f}")

    return expenses

def main():
    print(f'Running Expense Tracker!')
    expenseFilePath = "expense.csv"
    budget = 2000  

    expense = getUserExpense()
    saveExpenseToFile(expense, expenseFilePath)
    summarizeExpenses(expenseFilePath, budget)
    exportExpensesToExcel(expenseFilePath, budget)

if __name__ == "__main__":
    main()
