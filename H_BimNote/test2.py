import tkinter as tk
from tkinter import ttk
from tksheet import Sheet, num2alpha as n2a
import openpyxl

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# from src.views.widget.sheet_utils import SheetSearchManager


class SearchManager:
    def __init__(self, parent_frame, sheet_widget):
        """
        Initialize the SearchManager.
        :param parent_frame: The parent frame where the search UI components will be added.
        :param sheet_widget: The tksheet widget to which search functionality will be applied.
        """
        self.sheet = sheet_widget
        self.parent_frame = parent_frame

        # Create search UI components
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            parent_frame, textvariable=self.search_var, width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = ttk.Button(
            parent_frame, text="Search", command=self.search_sheet
        )
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(
            parent_frame, text="Clear Search", command=self.clear_search
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Bind Enter key to search functionality
        self.search_entry.bind("<Return>", lambda event: self.search_sheet())

    def search_sheet(self):
        """Search for rows containing the search term."""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.sheet.display_rows("all")  # Show all rows if search is empty
            self.sheet.redraw()  # Refresh the sheet immediately
            return

        sheet_data = self.sheet.get_sheet_data()
        matching_rows = [
            rn
            for rn, row in enumerate(sheet_data)
            if any(search_term in str(cell).lower() for cell in row)
        ]

        self.sheet.display_rows(rows=matching_rows, all_displayed=False)
        self.sheet.redraw()  # Refresh the sheet immediately
        print(f"Search term '{search_term}' found in rows: {matching_rows}")

    def clear_search(self):
        """Clear the search field and reset the displayed rows."""
        self.search_var.set("")
        self.sheet.display_rows("all")
        self.sheet.redraw()  # Refresh the sheet immediately


class ExcelSheetWidget(ttk.Frame):
    def __init__(self, parent, excel_file, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.excel_file = excel_file
        self.data = []
        self.column_headers = []

        # Load Excel data
        self.load_excel_data()

        # Create a frame for the top controls (button)
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X, pady=5)

        # Add "Clear Filters" button at the top
        self.clear_button = ttk.Button(
            self.control_frame, text="Clear Filters", command=self.clear_filters
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Initialize tksheet widget
        self.sheet = Sheet(
            self,
            data=self.data,
            column_width=180,
            # theme="dark",
            # theme="light green",
            height=500,
            width=1000,
        )
        self.sheet.enable_bindings(
            "copy",
            "rc_select",
            "arrowkeys",
            "double_click_column_resize",
            "column_width_resize",
            "column_select",
            "row_select",
            "drag_select",
            "single_select",
            "select_all",
        )

        self.sheet.set_options(header_font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(set_all_heights_and_widths=True)
        self.sheet.set_all_cell_sizes_to_text()

        self.sheet.pack(fill=tk.BOTH, expand=True)

        # Add header dropdowns
        self.add_dropdowns()

        # Add search functionality
        self.search_manager = SearchManager(self.control_frame, self.sheet)

    def load_excel_data(self):
        """Load data from Excel file and set headers and data."""
        try:
            workbook = openpyxl.load_workbook(self.excel_file, data_only=True)
            sheet = workbook.active

            # Extract headers
            self.column_headers = [
                cell.value if cell.value is not None else "" for cell in sheet[1]
            ]

            # Extract data
            self.data = [
                [cell.value if cell.value is not None else "" for cell in row]
                for row in sheet.iter_rows(min_row=2)
            ]
        except Exception as e:
            print(f"Error loading Excel file: {e}")

    def add_dropdowns(self):
        """Add dropdowns dynamically to each header without resetting existing selections."""
        current_headers = self.sheet.headers()  # Get current header values

        for col_idx, header in enumerate(self.column_headers):
            # Use sheet data to compute unique dropdown options
            sheet_data = self.sheet.get_sheet_data()
            unique_values = ["all"] + sorted(
                set(row[col_idx] for row in sheet_data if row[col_idx] is not None)
            )

            # Preserve the current header value
            current_value = (
                current_headers[col_idx] if col_idx < len(current_headers) else "all"
            )

            # Re-add the dropdown with the preserved value
            self.sheet.dropdown(
                self.sheet.span(n2a(col_idx), header=True, table=False),
                values=unique_values,
                set_value=current_value,  # Preserve the current selection
                selection_function=lambda event, col=col_idx: self.header_dropdown_selected(
                    event, col
                ),
                text=header,
            )

    def header_dropdown_selected(self, event, col_index):
        """Filter rows based on header dropdown selection."""
        self.sheet.redraw()
        hdrs = self.sheet.headers()
        print(hdrs)
        hdrs[event.loc] = event.value

        if all(dd == "all" for dd in hdrs):  # No filters applied
            self.sheet.display_rows("all")
        else:  # Apply filters
            rows = [
                rn
                for rn, row in enumerate(self.data)
                if all(row[c] == e or e == "all" for c, e in enumerate(hdrs))
            ]
            self.sheet.display_rows(rows=rows, all_displayed=False)

        # Recompute dropdown options based on filtered data
        self.add_dropdowns()

        self.sheet.redraw()

        # print(hdrs)

    def clear_filters(self):
        """Clear all filters and reset the table to show all data."""
        # Reset all headers to "all"
        hdrs = ["all"] * len(self.column_headers)
        self.sheet.headers(hdrs)

        # Display all rows
        self.sheet.display_rows("all")

        # Recompute dropdown options based on the full dataset
        self.add_dropdowns()

        self.sheet.redraw()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Excel Data Viewer with Filters")
    root.geometry("1200x600")

    # Replace with your Excel file path
    excel_file_path = "SACE2__excel_qty_result_0121-022123.xlsx"

    # Create and pack the ExcelSheetWidget
    excel_widget = ExcelSheetWidget(root, excel_file_path)
    excel_widget.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
