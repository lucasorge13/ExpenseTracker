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
        self.expenses = []
        self.budget = 2000
        self.budget_var = tk.DoubleVar(value=self.budget)

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
        self.create_expense_table()
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
        self.category_menu = ttk.OptionMenu(entry_frame, self.category_var, self.category_options[0], *self.category_options)
        self.category_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        add_button = ttk.Button(entry_frame, text="Add Expense", command=self.validate_and_add_expense)
        add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def validate_and_add_expense(self):
        name = self.expense_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()

        if not name or not amount:
            messagebox.showerror("Input Error", "Expense name and amount are required.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric amount.")
            return

        if amount <= 0:
            messagebox.showerror("Input Error", "Amount should be greater than zero.")
            return

        self.add_expense_to_file(name, category, amount)
        self.load_expenses()
        self.update_summary()
        self.update_charts()

    def add_expense_to_file(self, name, category, amount):
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
        add_expense(self.expenseFilePath, date, name, category, amount)
        messagebox.showinfo("Success", f"Added {name} to expenses.")

    def create_summary_frame(self):
        summary_frame = ttk.LabelFrame(self.root, text="Summary", padding=(10, 10))
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(summary_frame, textvariable=self.total_spent_var).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(summary_frame, textvariable=self.remaining_budget_var).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Budget entry and progress bar
        ttk.Label(summary_frame, text="Set Budget:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.budget_entry = ttk.Entry(summary_frame, textvariable=self.budget_var, width=20)
        self.budget_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.progress = ttk.Progressbar(summary_frame, length=200, maximum=self.budget, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        self.update_progress_bar()

        # Button to update the budget
        budget_button = ttk.Button(summary_frame, text="Update Budget", command=self.update_budget)
        budget_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    def update_budget(self):
        try:
            self.budget = float(self.budget_var.get())
            self.progress.config(maximum=self.budget)
            self.update_summary()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric budget.")

    def create_chart_frame(self):
        # Frame for the Pie Chart
        pie_chart_frame = ttk.LabelFrame(self.root, text="Expenses by Category", padding=(10, 10))
        pie_chart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.fig_pie, self.ax_pie = plt.subplots(figsize=(6, 5))
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, master=pie_chart_frame)
        self.canvas_pie.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Frame for the Bar Chart
        bar_chart_frame = ttk.LabelFrame(self.root, text="Expenses by Month", padding=(10, 10))
        bar_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.fig_bar, self.ax_bar = plt.subplots(figsize=(6, 5))
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=bar_chart_frame)
        self.canvas_bar.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_charts()

    def create_expense_table(self):
        table_frame = ttk.LabelFrame(self.root, text="Recorded Expenses", padding=(10, 10))
        table_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(table_frame, columns=("Date", "Name", "Category", "Amount"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_item_selected)

    def on_item_selected(self, event):
        selected_item = self.tree.selection()[0]
        item_data = self.tree.item(selected_item, "values")

        name = item_data[1]
        amount = item_data[3]
        category = item_data[2]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")

        ttk.Label(edit_window, text="Expense Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(edit_window, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        name_entry.insert(0, name)

        ttk.Label(edit_window, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        amount_entry = ttk.Entry(edit_window, width=30)
        amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        amount_entry.insert(0, amount)

        ttk.Label(edit_window, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        category_var = tk.StringVar(value=category)
        category_menu = ttk.OptionMenu(edit_window, category_var, category, *self.category_options)
        category_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        def save_changes():
            new_name = name_entry.get().strip()
            new_amount = amount_entry.get().strip()
            new_category = category_var.get()

            if not new_name or not new_amount:
                messagebox.showerror("Input Error", "Expense name and amount are required.")
                return

            try:
                new_amount = float(new_amount)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric amount.")
                return

            if new_amount <= 0:
                messagebox.showerror("Input Error", "Amount should be greater than zero.")
                return
             # Update the treeview with the new data
            self.tree.item(selected_item, values=(item_data[0], new_name, new_category, new_amount))

            # Reflect changes in the CSV file
            df = pd.DataFrame(self.expenses)
            df.loc[df.index[int(selected_item)], ["Expense Name", "Category", "Amount"]] = [new_name, new_category, new_amount]
            df.to_csv(self.expenseFilePath, index=False)

            self.load_expenses()
            self.update_summary()
            self.update_charts()

            edit_window.destroy()

        def delete_expense():
            # Remove from Treeview
            self.tree.delete(selected_item)

            # Reflect changes in the CSV file
            df = pd.DataFrame(self.expenses)
            df = df.drop(df.index[int(selected_item)])
            df.to_csv(self.expenseFilePath, index=False)

            self.load_expenses()
            self.update_summary()
            self.update_charts()

            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        delete_button = ttk.Button(edit_window, text="Delete Expense", command=delete_expense)
        delete_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

    def update_charts(self):
        if not self.expenses:
            return

        # Clear previous figures
        self.ax_pie.clear()
        self.ax_bar.clear()

        df = pd.DataFrame(self.expenses)
        
        # Convert Amount column to numeric, forcing errors to NaN and then dropping them
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        
        # Drop any rows where Amount could not be converted to a float
        df = df.dropna(subset=["Amount"])

        # Convert Date to datetime format for easier manipulation
        df["Date"] = pd.to_datetime(df["Date"])

        # Group by category and sum the amounts for the pie chart
        category_totals = df.groupby("Category")["Amount"].sum()

        # Plot the pie chart
        self.ax_pie.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
        self.ax_pie.set_title("Expenses by Category")

        # Group by month and sum the amounts for the bar chart
        df["Month"] = df["Date"].dt.to_period("M")
        monthly_totals = df.groupby("Month")["Amount"].sum()

        # Plot the bar chart
        monthly_totals.plot(kind="bar", ax=self.ax_bar, color="skyblue", edgecolor="black")
        self.ax_bar.set_title("Expenses by Month")
        self.ax_bar.set_xlabel("Month")
        self.ax_bar.set_ylabel("Total Expenses")

        # Redraw the canvases with the updated figures
        self.canvas_pie.draw()
        self.canvas_bar.draw()

    def load_expenses(self):
        self.expenses = load_expenses(self.expenseFilePath)
        self.tree.delete(*self.tree.get_children())  # Clear the treeview

        for i, expense in enumerate(self.expenses):
            self.tree.insert('', 'end', iid=i, values=(expense["Date"], expense["Expense Name"], expense["Category"], expense["Amount"]))

    def update_summary(self):
        total_spent = sum(float(exp["Amount"]) for exp in self.expenses)
        remaining_budget = self.budget - total_spent
        self.total_spent_var.set(f"Total Spent: ${total_spent:.2f}")
        self.remaining_budget_var.set(f"Remaining Budget: ${remaining_budget:.2f}")

        # Update the progress bar
        self.update_progress_bar()

    def update_progress_bar(self):
        total_spent = sum(float(exp["Amount"]) for exp in self.expenses)
        self.progress['value'] = total_spent

    def create_export_button(self):
        export_button = ttk.Button(self.root, text="Export to Excel", command=self.export_to_excel)
        export_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def export_to_excel(self):
        export_expenses_to_excel(self.expenses)
        messagebox.showinfo("Export Successful", "Expenses have been exported to expense_summary.xlsx.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
