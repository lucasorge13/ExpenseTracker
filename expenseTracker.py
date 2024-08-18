import os
from expense import add_expense, load_expenses
from excel_exporter import export_expenses_to_excel

def main():
    print("Running Expense Tracker!")
    expenseFilePath = "expense.csv"
    budget = 2000  # Example budget, this could be user-defined

    print("Getting User Expense!")
    expense_name = input("Enter expense name: ").strip()
    expense_amount = input("Enter expense amount: ").strip()

    if not expense_name or not expense_amount:
        print("Error: Expense name and amount are required.")
        return

    try:
        expense_amount = float(expense_amount)
    except ValueError:
        print("Error: Invalid amount entered. Please enter a numeric value.")
        return

    categories = ["Food", "Rent", "Utilities", "Transportation", "Entertainment", "Other"]
    print("Available categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")

    category_choice = input("Select a category number: ").strip()
    if not category_choice.isdigit() or not 1 <= int(category_choice) <= len(categories):
        print("Error: Invalid category choice.")
        return

    category = categories[int(category_choice) - 1]

    # Add expense
    add_expense(expenseFilePath, "2023-08-10", expense_name, category, expense_amount)

    # Load and summarize expenses
    print("Summarizing expenses from expense.csv...")
    expenses = load_expenses(expenseFilePath)
    total_spent = sum(float(exp["Amount"]) for exp in expenses)
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Budget: ${budget:.2f}")
    print(f"Remaining: ${budget - total_spent:.2f}")

    # Export expenses to Excel
    print("Exporting expenses to Excel...")
    export_expenses_to_excel(expenses)
    print("Expenses have been exported to expense_summary.xlsx.")

if __name__ == "__main__":
    main()