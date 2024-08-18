import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import numpy as np
import pandas as pd
from excel_exporter import export_expenses_to_excel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg='#f7f7f7')
        self.root.state('zoomed') # Make the GUI full screen

        # Initialize attributes
        self.expenseFilePath = "expense.csv"
        self.budget = 2000
        self.expenses = []

        # Initialize Tkinter variables
        self.category_var = tk.StringVar()
        self.total_spent_var = tk.StringVar(value="Total Spent: $0.00")
        self.remaining_budget_var = tk.StringVar(value="Remaining Budget: $0.00")

        # Initialize category options
        self.category_options = ["Food", "Rent", "Utilities", "Transportation", "Entertainment", "Other"]

        # Create tab control
        self.tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.create_tabs()

        # # Create widgets
        # self.create_widgets()

        # Load data and update summary
        self.load_expenses()
        self.update_summary()

    def create_tabs(self):
        # Tab for Pie Chart
        self.pie_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.pie_tab, text="Pie Chart")
        self.tab_control.pack(expand=1, fill="both")

        # Tab for Bar Chart
        self.bar_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.bar_tab, text="Monthly Trends")
        self.tab_control.pack(expand=1, fill="both")

        # Tab for Stacked Bar Chart
        self.stacked_bar_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.stacked_bar_tab, text="Category Contributions")
        self.tab_control.pack(expand=1, fill="both")

        # Create widgets in the tabs
        self.create_pie_chart_tab()
        self.create_bar_chart_tab()
        self.create_stacked_bar_chart_tab()

    def create_pie_chart_tab(self):
        # Expense Summary Section
        summary_frame = ttk.LabelFrame(self.pie_tab, text="Expense Summary", padding=(10, 10))
        summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.total_spent_label = ttk.Label(summary_frame, textvariable=self.total_spent_var, font=('Arial', 10, 'bold'))
        self.remaining_budget_label = ttk.Label(summary_frame, textvariable=self.remaining_budget_var, font=('Arial', 10, 'bold'))
        self.total_spent_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.remaining_budget_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Chart Section
        self.chart_frame = ttk.LabelFrame(self.pie_tab, text="Expense Chart", padding=(10, 10))
        self.chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.pie_tab.grid_rowconfigure(1, weight=1)
        self.pie_tab.grid_columnconfigure(0, weight=1)

    def create_bar_chart_tab(self):
        self.bar_chart_frame = ttk.LabelFrame(self.bar_tab, text="Monthly Expense Trends", padding=(10, 10))
        self.bar_chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.bar_tab.grid_rowconfigure(0, weight=1)
        self.bar_tab.grid_columnconfigure(0, weight=1)

    def create_stacked_bar_chart_tab(self):
        self.stacked_bar_chart_frame = ttk.LabelFrame(self.stacked_bar_tab, text="Category Contributions", padding=(10, 10))
        self.stacked_bar_chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.stacked_bar_tab.grid_rowconfigure(0, weight=1)
        self.stacked_bar_tab.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        # Expense Entry Section
        entry_frame = ttk.LabelFrame(self.root, text="Add New Expense", padding=(10, 10))
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Expense Name
        ttk.Label(entry_frame, text="Expense Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.expense_entry = ttk.Entry(entry_frame, width=30)
        self.expense_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Expense Amount
        ttk.Label(entry_frame, text="Expense Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(entry_frame, width=30)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Category Dropdown
        ttk.Label(entry_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.category_dropdown = ttk.Combobox(entry_frame, textvariable=self.category_var, values=self.category_options, state="readonly", width=28)
        self.category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Add Expense Button
        self.add_button = ttk.Button(entry_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Expense Summary Section
        summary_frame = ttk.LabelFrame(self.root, text="Expense Summary", padding=(10, 10))
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.total_spent_label = ttk.Label(summary_frame, textvariable=self.total_spent_var, font=('Arial', 10, 'bold'))
        self.remaining_budget_label = ttk.Label(summary_frame, textvariable=self.remaining_budget_var, font=('Arial', 10, 'bold'))
        self.total_spent_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.remaining_budget_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Expense List and Edit/Delete Options
        list_frame = ttk.LabelFrame(self.root, text="Manage Expenses", padding=(10, 10))
        list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.expense_listbox = tk.Listbox(list_frame, height=10, width=50)
        self.expense_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.expense_listbox.bind("<<ListboxSelect>>", self.on_select_expense)

        edit_button = ttk.Button(list_frame, text="Edit Expense", command=self.edit_expense)
        delete_button = ttk.Button(list_frame, text="Delete Expense", command=self.delete_expense)
        edit_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        delete_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Chart Section
        chart_frame = ttk.LabelFrame(self.root, text="Expense Chart", padding=(10, 10))
        chart_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.chart_frame = chart_frame  # Save for later updates

        # Export to Excel Button
        self.export_button = ttk.Button(self.root, text="Export to Excel", command=self.export_to_excel)
        self.export_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid weights for resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=3)  # Give more space to the chart
        self.root.grid_rowconfigure(4, weight=0)

        entry_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(0, weight=1)
        chart_frame.grid_columnconfigure(0, weight=1)

    def load_expenses(self):
        # Load expenses from CSV or initialize an empty list if file doesn't exist
        try:
            self.expenses = pd.read_csv(self.expenseFilePath).to_dict('records')
        except FileNotFoundError:
            self.expenses = []

    def refresh_expense_list(self):
        self.expense_listbox.delete(0, tk.END)
        for i, expense in enumerate(self.expenses):
            self.expense_listbox.insert(tk.END, f"{expense['Expense Name']} - {expense['Category']} - ${expense['Amount']}")

    def on_select_expense(self, event):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_expense = self.expenses[selected_index]
            self.expense_entry.delete(0, tk.END)
            self.expense_entry.insert(0, selected_expense["Expense Name"])
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, selected_expense["Amount"])
            self.category_var.set(selected_expense["Category"])

    def edit_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            self.expenses[selected_index] = {
                "Expense Name": self.expense_entry.get(),
                "Category": self.category_var.get(),
                "Amount": self.amount_entry.get(),
            }
            self.save_expenses()
            self.load_expenses()
            self.update_summary()
            messagebox.showinfo("Success", "Expense updated successfully!")

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            del self.expenses[selected_index]
            self.save_expenses()
            self.load_expenses()
            self.update_summary()
            messagebox.showinfo("Success", "Expense deleted successfully!")

    def save_expenses(self):
        with open(self.expenseFilePath, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Expense Name", "Category", "Amount"])
            writer.writeheader()
            writer.writerows(self.expenses)

    def update_summary(self):
        total_spent = sum(float(expense["Amount"]) for expense in self.expenses)
        remaining_budget = self.budget - total_spent
        self.total_spent_var.set(f"Total Spent: ${total_spent:.2f}")
        self.remaining_budget_var.set(f"Remaining Budget: ${remaining_budget:.2f}")
        self.update_pie_chart()
        self.update_bar_chart()
        self.update_stacked_bar_chart()

    def update_bar_chart(self):
        for widget in self.bar_chart_frame.winfo_children():
            widget.destroy()

        df = pd.DataFrame(self.expenses)

        # Check if 'Date' column exists and handle missing dates
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Date'] = df['Date'].fillna(pd.to_datetime('today'))  # Fill NaN dates with today's date
            df.set_index('Date', inplace=True)
            monthly_sums = df.resample('ME').sum()

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(monthly_sums.index, monthly_sums['Amount'], color=plt.cm.Pastel1.colors)

            ax.set_title('Monthly Expense Trends')
            ax.set_xlabel('Month')
            ax.set_ylabel('Total Expense ($)')
            ax.grid(True)
        else:
            # Handle case where 'Date' column is missing entirely
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df.index, df['Amount'], color=plt.cm.Pastel1.colors)

            ax.set_title('Expense Trends')
            ax.set_xlabel('Entry')
            ax.set_ylabel('Total Expense ($)')
            ax.grid(True)

        chart = FigureCanvasTkAgg(fig, self.bar_chart_frame)
        chart.get_tk_widget().pack()
        chart.draw()

    def update_pie_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        categories = [expense["Category"] for expense in self.expenses]
        amounts = [float(expense["Amount"]) for expense in self.expenses]
        remaining_budget = self.budget - sum(amounts)

        if remaining_budget > 0:
            categories.append("Remaining Budget")
            amounts.append(remaining_budget)

        # Initialize the dictionary with all categories
        category_sums = {}
        for category in categories:
            if category not in category_sums:
                category_sums[category] = 0

        # Sum the amounts by category
        for category, amount in zip(categories, amounts):
            category_sums[category] += amount

        # Separate the categories and amounts after aggregation
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

    def update_stacked_bar_chart(self):
        for widget in self.stacked_bar_chart_frame.winfo_children():
            widget.destroy()

        df = pd.DataFrame(self.expenses)

        # Check if 'Date' column exists and handle missing dates
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Date'] = df['Date'].fillna(pd.to_datetime('today'))  # Fill NaN dates with today's date
            df.set_index('Date', inplace=True)
            df_pivot = df.pivot_table(values='Amount', index=df.index.month, columns='Category', aggfunc='sum')

            fig, ax = plt.subplots(figsize=(10, 5))
            df_pivot.plot(kind='bar', stacked=True, ax=ax, color=plt.cm.Pastel1.colors)

            ax.set_title('Category Contributions Over Months')
            ax.set_xlabel('Month')
            ax.set_ylabel('Total Expense ($)')
            ax.grid(True)
        else:
            # Handle case where 'Date' column is missing
            messagebox.showerror("Error", "The 'Date' column is missing from the CSV file. Unable to create the stacked bar chart.")
            return

        chart = FigureCanvasTkAgg(fig, self.stacked_bar_chart_frame)
        chart.get_tk_widget().pack()
        chart.draw()

    def update_chart(self):
        # Clear the existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Prepare data for the pie chart
        categories = [expense["Category"] for expense in self.expenses]
        amounts = [float(expense["Amount"]) for expense in self.expenses]
        remaining_budget = self.budget - sum(amounts)
        
        # Adding the remaining budget to the chart
        if remaining_budget > 0:
            categories.append("Remaining Budget")
            amounts.append(remaining_budget)
        
        # Aggregate the amounts by category
        category_sums = {}
        for category, amount in zip(categories, amounts):
            if category in category_sums:
                category_sums[category] += amount
            else:
                category_sums[category] = amount

        # Separate the categories and amounts after aggregation
        categories = list(category_sums.keys())
        amounts = list(category_sums.values())

        # Custom colors for the pie chart
        colors = plt.cm.Paired.colors

        # Highlight "Remaining Budget" with a different color
        highlight_color = 'red'
        if "Remaining Budget" in categories:
            idx = categories.index("Remaining Budget")
            colors = list(colors)
            colors[idx] = highlight_color

        # Generate the pie chart with a small offset for "Remaining Budget"
        explode = [0.1 if cat == "Remaining Budget" else 0 for cat in categories]

        fig, ax = plt.subplots(figsize=(7, 7), dpi=100)
        wedges, texts = ax.pie(amounts, explode=explode, colors=colors, startangle=90)

        # Calculate and position percentages manually
        for i, wedge in enumerate(wedges):
            percentage = f'{amounts[i]/sum(amounts)*100:.1f}%'
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = 1.2 * np.cos(np.radians(angle))
            y = 1.2 * np.sin(np.radians(angle))
            ax.text(x, y, percentage, ha='center', va='center')

        # Add a legend with the categories
        ax.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Highlight the remaining budget slice
        for i, wedge in enumerate(wedges):
            if categories[i] == "Remaining Budget":
                wedge.set_edgecolor('black')
                wedge.set_linewidth(2)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

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
            export_expenses_to_excel(self.expenseFilePath, self.budget)
            messagebox.showinfo("Success", "Expenses have been exported to Excel.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export expenses: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
