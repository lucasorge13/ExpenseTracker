import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from excel_exporter import exportExpensesToExcel

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        # Set up the layout
        self.create_widgets()
        
        # Expense file path and budget
        self.expenseFilePath = "expense.csv"
        self.budget = 2000  # Placeholder budget, can be changed

    def create_widgets(self):
        # Expense Name
        self.expense_label = ttk.Label(self.root, text="Expense Name:")
        self.expense_label.grid(row=0, column=0, padx=10, pady=10)
        self.expense_entry = ttk.Entry(self.root, width=30)
        self.expense_entry.grid(row=0, column=1, padx=10, pady=10)

        # Expense Amount
        self.amount_label = ttk.Label(self.root, text="Expense Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self.root, width=30)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Category Dropdown
        self.category_label = ttk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=10)
        self.category_options = ["Food", "Rent", "Utilities", "Transportation", "Entertainment", "Other"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var, values=self.category_options, state="readonly", width=28)
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.category_dropdown.current(0)  # Default to first category

        # Add Expense Button
        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)

        # Export to Excel Button
        self.export_button = ttk.Button(self.root, text="Export to Excel", command=self.export_to_excel)
        self.export_button.grid(row=3, column=1, padx=10, pady=10)

    def add_expense(self):
        name = self.expense_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()

        if not name or not amount:
            messagebox.showerror("Input Error", "Please provide both an expense name and amount.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive number for the amount.")
            return

        # Save expense to CSV file
        self.save_expense_to_file({"name": name, "category": category, "amount": amount})

        # Clear the entry fields
        self.expense_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.current(0)

        messagebox.showinfo("Success", "Expense added successfully!")

    def save_expense_to_file(self, expense):
        file_exists = os.path.isfile(self.expenseFilePath)
        with open(self.expenseFilePath, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Expense Name", "Category", "Amount"])
            writer.writerow([expense["name"], expense["category"], expense["amount"]])

    def export_to_excel(self):
        try:
            exportExpensesToExcel(self.expenseFilePath, self.budget)
            messagebox.showinfo("Success", "Expenses have been exported to Excel.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export expenses: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
