import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from excel_exporter import export_expenses_to_excel
from expense import load_expenses, add_expense

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg='#f7f7f7')
        self.root.state('zoomed')  # Full screen

        self.expenseFilePath = "expense.csv"
        self.budget = 2000
        self.expenses = []

        self.category_var = tk.StringVar()
        self.total_spent_var = tk.StringVar(value="Total Spent: $0.00")
        self.remaining_budget_var = tk.StringVar(value="Remaining Budget: $0.00")

        self.category_options = ["Food", "Rent", "Utilities", "Transportation", "Entertainment", "Other"]

        # Initialize GUI components
        self.create_widgets()
        self.load_expenses()
        self.update_summary()

    def create_widgets(self):
        self.create_entry_frame()
        self.create_summary_frame()
        self.create_chart_frame()
        self.create_export_button()

    def create_entry_frame(self):
        entry_frame = ttk.LabelFrame(self.root, text="Add New Expense", padding=(10, 10))
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(entry_frame, text="Expense Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.expense_entry = ttk.Entry(entry_frame, width=30)
        self.expense_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(entry_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(entry_frame, width=30)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(entry_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.category_dropdown = ttk.Combobox(entry_frame, textvariable=self.category_var, values=self.category_options, state="readonly", width=28)
        self.category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.category_dropdown.current(0)  # Default to first category

        add_button = ttk.Button(entry_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    def create_summary_frame(self):
        summary_frame = ttk.LabelFrame(self.root, text="Expense Summary", padding=(10, 10))
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.total_spent_label = ttk.Label(summary_frame, textvariable=self.total_spent_var, font=('Arial', 10, 'bold'))
        self.remaining_budget_label = ttk.Label(summary_frame, textvariable=self.remaining_budget_var, font=('Arial', 10, 'bold'))
        self.total_spent_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.remaining_budget_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def create_chart_frame(self):
        self.chart_frame = ttk.LabelFrame(self.root, text="Expense Chart", padding=(10, 10))
        self.chart_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_export_button(self):
        self.export_button = ttk.Button(self.root, text="Export to Excel", command=self.export_expenses)
        self.export_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def load_expenses(self):
        self.expenses = load_expenses(self.expenseFilePath)

    def add_expense(self):
        date = tk.StringVar(value="2023-08-10")  # Default date, this can be made dynamic
        name = self.expense_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()

        if not name or not amount or not category:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        add_expense(self.expenseFilePath, date.get(), name, category, amount)
        self.load_expenses()
        self.update_summary()
        self.clear_inputs()

    def update_summary(self):
        total_spent = sum(float(expense["Amount"]) for expense in self.expenses)
        remaining_budget = self.budget - total_spent
        self.total_spent_var.set(f"Total Spent: ${total_spent:.2f}")
        self.remaining_budget_var.set(f"Remaining Budget: ${remaining_budget:.2f}")
        self.update_pie_chart()

    def update_pie_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        categories = [expense["Category"] for expense in self.expenses]
        amounts = [float(expense["Amount"]) for expense in self.expenses]
        remaining_budget = self.budget - sum(amounts)

        if remaining_budget > 0:
            categories.append("Remaining Budget")
            amounts.append(remaining_budget)

        category_sums = {}
        for category, amount in zip(categories, amounts):
            if category not in category_sums:
                category_sums[category] = 0
            category_sums[category] += amount

        categories = list(category_sums.keys())
        amounts = list(category_sums.values())

        pastel_colors = plt.cm.Pastel1.colors
        colors = pastel_colors[:len(categories)]

        explode = [0.1 if cat == "Remaining Budget" else 0 for cat in categories]

        fig, ax = plt.subplots(figsize=(7, 7), dpi=100)
        wedges, texts = ax.pie(amounts, explode=explode, colors=colors, startangle=90)

        for i, wedge in enumerate(wedges):
            percentage = f'{amounts[i]/sum(amounts)*100:.1f}%'
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = 1.2 * np.cos(np.radians(angle))
            y = 1.2 * np.sin(np.radians(angle))
            ax.text(x, y, percentage, ha='center', va='center')

        ax.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        for i, wedge in enumerate(wedges):
            if categories[i] == "Remaining Budget":
                wedge.set_edgecolor('black')
                wedge.set_linewidth(2)

        ax.axis('equal')
        chart = FigureCanvasTkAgg(fig, self.chart_frame)
        chart.get_tk_widget().pack()
        chart.draw()

    def clear_inputs(self):
        self.expense_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.current(0)

    def export_expenses(self):
        export_expenses_to_excel(self.expenses)
        messagebox.showinfo("Export Complete", "Expenses have been successfully exported to Excel.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()