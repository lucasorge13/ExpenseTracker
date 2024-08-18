import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from excel_exporter import exportExpensesToExcel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        # Set up the layout
        self.create_widgets()
        
        # Expense file path and budget
        self.expenseFilePath = "expense.csv"
        self.budget = 2000  # Placeholder budget, can be changed
        
        # Initialize expense data
        self.expenses = []
        self.load_expenses()
        self.update_summary()

    def create_widgets(self):
        # Expense Entry Section
        entry_frame = ttk.LabelFrame(self.root, text="Add New Expense")
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Expense Name
        ttk.Label(entry_frame, text="Expense Name:").grid(row=0, column=0, padx=10, pady=10)
        self.expense_entry = ttk.Entry(entry_frame, width=30)
        self.expense_entry.grid(row=0, column=1, padx=10, pady=10)

        # Expense Amount
        ttk.Label(entry_frame, text="Expense Amount:").grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(entry_frame, width=30)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Category Dropdown
        ttk.Label(entry_frame, text="Category:").grid(row=2, column=0, padx=10, pady=10)
        self.category_options = ["Food", "Rent", "Utilities", "Transportation", "Entertainment", "Other"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(entry_frame, textvariable=self.category_var, values=self.category_options, state="readonly", width=28)
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.category_dropdown.current(0)  # Default to first category

        # Add Expense Button
        self.add_button = ttk.Button(entry_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Expense Summary Section
        summary_frame = ttk.LabelFrame(self.root, text="Expense Summary")
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.total_spent_var = tk.StringVar(value="Total Spent: $0.00")
        self.remaining_budget_var = tk.StringVar(value="Remaining Budget: $0.00")
        self.total_spent_label = ttk.Label(summary_frame, textvariable=self.total_spent_var)
        self.remaining_budget_label = ttk.Label(summary_frame, textvariable=self.remaining_budget_var)
        self.total_spent_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.remaining_budget_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Chart Section
        chart_frame = ttk.LabelFrame(self.root, text="Expense Chart")
        chart_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.chart_frame = chart_frame  # Save for later updates

        # Export to Excel Button
        self.export_button = ttk.Button(self.root, text="Export to Excel", command=self.export_to_excel)
        self.export_button.grid(row=3, column=0, padx=10, pady=10)

    def load_expenses(self):
        if os.path.exists(self.expenseFilePath):
            with open(self.expenseFilePath, "r") as file:
                reader = csv.DictReader(file)
                self.expenses = [row for row in reader]
    
    def update_summary(self):
        total_spent = sum(float(expense["Amount"]) for expense in self.expenses)
        remaining_budget = self.budget - total_spent
        self.total_spent_var.set(f"Total Spent: ${total_spent:.2f}")
        self.remaining_budget_var.set(f"Remaining Budget: ${remaining_budget:.2f}")
        self.update_chart()

    def update_chart(self):
        # Clear the existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Prepare data for the pie chart
        categories = [expense["Category"] for expense in self.expenses]
        amounts = [float(expense["Amount"]) for expense in self.expenses]
        if not categories or not amounts:
            return

        # Generate the pie chart
        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        # Display the chart in the Tkinter window
        chart = FigureCanvasTkAgg(fig, self.chart_frame)
        chart.get_tk_widget().pack()
        chart.draw()

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

        # Update expense data and summary
        self.load_expenses()
        self.update_summary()

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
