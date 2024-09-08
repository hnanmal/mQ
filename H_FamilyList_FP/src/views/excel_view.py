#src/views/excel_view.py

import tkinter as tk
from tkinter import ttk
from tksheet import Sheet
from tksheet.other_classes import Box_nt
from openpyxl import load_workbook



def load_and_display_excel_with_search(parent):
    """Read the WorkMaster_DB.xlsx file using openpyxl and display it in tksheet with a search feature."""
    try:
        # Load the Excel file using openpyxl
        file_path = "resources/WorkMaster_DB.xlsx"
        workbook = load_workbook(file_path)
        sheet = workbook.active

        # Extract data from the active sheet
        data_ = []
        for row in sheet.iter_rows(values_only=True):
            data_.append(list(row))
        data = list(filter(lambda x: any(x)!=False, data_))

        # Create a frame for the search box and search button
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create the search entry box
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Create the search button
        search_button = ttk.Button(search_frame, text="Search", command=lambda: search_excel_data(sheet_widget, data, search_var.get()))
        search_button.pack(side=tk.LEFT, padx=5)

        # Create a tksheet widget for the Excel data
        sheet_widget = Sheet(parent)
        sheet_widget.pack(fill=tk.BOTH, expand=True)

        # Set headers and data
        headers = [str(cell) for cell in data[4]]  # First row as headers
        sheet_widget.headers(headers)
        sheet_widget.set_sheet_data(data[6:])  # Populate the data, skipping headers

        # Optionally hide specific columns
        sheet_widget.hide_columns([1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22])

        # Enable sheet functionality
        sheet_widget.disable_bindings()
        sheet_widget.enable_bindings(
            "single_select",  # Allow single cell selection
            "row_select",     # Allow row selection
            "column_select",  # Allow column selection
            "drag_select",    # Allow drag selection
        )

        # Bind the Enter key to trigger search functionality
        search_entry.bind("<Return>", lambda event: search_excel_data(sheet_widget, data, search_var.get()))

        return sheet_widget  # Return the sheet widget for use in other functions

    except FileNotFoundError:
        tk.Label(parent, text="WorkMaster_DB.xlsx not found").pack(pady=20)
    except Exception as e:
        tk.Label(parent, text=f"Error: {e}").pack(pady=20)

def search_excel_data(sheet_widget, original_data, search_text):
    """Filter the Excel rows based on the search text and update the sheet."""
    if not search_text:
        # If search text is empty, show all rows
        sheet_widget.set_sheet_data(original_data[6:])
    else:
        # Filter rows that contain the search text
        filtered_data = [
            row for row in original_data[6:] if any(search_text.lower() in str(cell).lower() for cell in row)
        ]
        # Update the sheet with the filtered data
        sheet_widget.set_sheet_data(filtered_data)