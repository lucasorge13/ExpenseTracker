from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import DataBarRule
import logging

# Set up logging
logging.basicConfig(filename='excel_exporter.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_workbook():
    """
    Create a new Excel workbook and return the active worksheet.
    
    Returns:
        tuple: Workbook and worksheet objects.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Expense Summary"
    return wb, ws

def style_headers(ws):
    """
    Style the headers of the Excel sheet.
    
    Args:
        ws (Worksheet): The active worksheet.
    """
    header_font = Font(bold=True, color="FFFFFF")
    fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    alignment = Alignment(horizontal="center", vertical="center")

    for col_num, column_title in enumerate(ws.iter_cols(1, ws.max_column), 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = fill
        cell.alignment = alignment
        ws.column_dimensions[get_column_letter(col_num)].width = 20

def add_conditional_formatting(ws):
    """
    Add conditional formatting to the Excel sheet.
    
    Args:
        ws (Worksheet): The active worksheet.
    """
    data_bar_rule = DataBarRule(start_type="min", end_type="max", color="63C384")
    ws.conditional_formatting.add(f"B2:B{ws.max_row}", data_bar_rule)

def export_expenses_to_excel(expenses, file_path="expense_summary.xlsx"):
    """
    Export expenses data to an Excel file with enhanced styling and formatting.
    
    Args:
        expenses (list of dict): A list of expense records.
        file_path (str): The path to save the Excel file.
    """
    try:
        wb, ws = create_workbook()
        
        # Write headers
        headers = ["Date", "Expense Name", "Category", "Amount"]
        ws.append(headers)

        # Write data rows
        for expense in expenses:
            ws.append([expense.get(header, "") for header in headers])

        # Apply styling
        style_headers(ws)
        add_conditional_formatting(ws)

        # Save workbook
        wb.save(file_path)
        logging.info(f"Expenses exported successfully to {file_path}.")
        print(f"Expenses exported successfully to {file_path}.")

    except Exception as e:
        logging.exception(f"Failed to export expenses: {str(e)}")
        print(f"Error: Failed to export expenses: {str(e)}")

# Example usage
if __name__ == "__main__":
    example_expenses = [
        {"Date": "2023-08-01", "Expense Name": "Groceries", "Category": "Food", "Amount": 150},
        {"Date": "2023-08-02", "Expense Name": "Rent", "Category": "Housing", "Amount": 1200},
        # Add more expenses as needed
    ]
    export_expenses_to_excel(example_expenses)
