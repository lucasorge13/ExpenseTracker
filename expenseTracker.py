from expense import Expense
from excel_exporter import exportExpensesToExcel

def main():
    print(f'Running Expense Tracker!')
    expenseFilePath = "expense.csv"
    budget = 2000  

    expense = getUserExpense()
    saveExpenseToFile(expense, expenseFilePath)
    summarizeExpenses(expenseFilePath, budget)
    exportExpensesToExcel(expenseFilePath, budget)

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
    with open(filePath, "a") as file:
        file.write(f"{expense.name},{expense.category},{expense.amount:.2f}\n")

def summarizeExpenses(filePath, budget):
    print(f"Summarizing expenses from {filePath}...")

    totalSpent = 0
    expenses = []

    with open(filePath, "r") as file:
        for line in file:
            name, category, amount = line.strip().split(",")
            amount = float(amount)
            totalSpent += amount
            expenses.append({"name": name, "category": category, "amount": amount})

    print(f"Total Spent: ${totalSpent:.2f}")
    print(f"Budget: ${budget:.2f}")
    print(f"Remaining: ${budget - totalSpent:.2f}")

    return expenses

if __name__ == "__main__":
    main()
