import tkinter as tk
from tksheet import Sheet
import openpyxl


class ExcelSheetWidget(tk.Frame):
    def __init__(self, parent, excel_file, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.excel_file = excel_file
        self.sheet_data = []
        self.filtered_data = []

        # Create a frame for the filter widgets
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        # Add filter widgets and clear button
        self.filter_entries = []
        self.column_headers = []  # Store column headers
        self.create_filter_widgets(filter_frame)

        # Add the "Clear Filter" button
        clear_button = tk.Button(
            filter_frame, text="Clear Filter", command=self.clear_filter
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        # Initialize tksheet widget
        self.sheet = Sheet(
            self,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            width=600,
            height=400,
        )
        self.sheet.pack(fill=tk.BOTH, expand=True)

        # Adjust font size (one step smaller)
        self.sheet.set_options(header_font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(font=("Arial", 8, "normal"))

        # Load and display Excel data
        self.load_excel_data()

    def create_filter_widgets(self, frame):
        """Create filter widgets for each column."""
        tk.Label(frame, text="Filter (Enter values and press Enter):").pack(
            side=tk.LEFT
        )
        for i in range(
            5
        ):  # Assume a maximum of 5 columns initially; update dynamically after loading Excel
            entry = tk.Entry(frame, width=15)
            entry.pack(side=tk.LEFT, padx=2)
            entry.bind("<Return>", self.apply_filter)  # Apply filter on Enter key press
            self.filter_entries.append(entry)

    def load_excel_data(self):
        """Load data from an Excel file and populate the tksheet."""
        try:
            # Load the Excel workbook
            workbook = openpyxl.load_workbook(self.excel_file, data_only=True)
            sheet = workbook.active

            # Read headers
            self.column_headers = [
                cell.value if cell.value is not None else "" for cell in sheet[1]
            ]
            for i, header in enumerate(self.column_headers):
                if i < len(
                    self.filter_entries
                ):  # Update filter widgets if there are fewer columns
                    self.filter_entries[i].delete(0, tk.END)
                    self.filter_entries[i].insert(0, f"{header}")

            # Read data into a list of lists
            self.sheet_data = [
                [cell.value if cell.value is not None else "" for cell in row]
                for row in sheet.iter_rows(min_row=2)
            ]
            self.filtered_data = self.sheet_data  # Start with all data displayed

            # Display the data in the tksheet widget
            self.sheet.headers(self.column_headers)
            self.sheet.set_sheet_data(
                self.filtered_data, reset_col_positions=True, reset_row_positions=True
            )
            self.sheet.enable_bindings()  # Enable all default bindings

            # Auto-adjust column widths using `column_width` method
            for col_index in range(len(self.column_headers)):
                self.sheet.column_width(col_index, width=150)

        except Exception as e:
            print(f"Error loading Excel file: {e}")

    def apply_filter(self, event=None):
        """Apply the filter based on the values in the filter entry widgets."""
        filters = [entry.get().strip().lower() for entry in self.filter_entries]
        self.filtered_data = [
            row
            for row in self.sheet_data
            if all(
                str(row[i]).lower().find(filters[i]) != -1 if filters[i] else True
                for i in range(len(filters))
            )
        ]
        self.refresh_filtered_data()

    def clear_filter(self):
        """Clear all filters and display the unfiltered data."""
        for entry in self.filter_entries:
            entry.delete(0, tk.END)  # Clear all filter entry fields
        self.filtered_data = self.sheet_data  # Reset to original data
        self.refresh_filtered_data()

    def refresh_filtered_data(self):
        """Refresh the tksheet widget with the filtered data."""
        self.sheet.set_sheet_data(
            self.filtered_data, reset_col_positions=True, reset_row_positions=True
        )


# Example usage in a standalone app
if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("Excel Data Viewer with Filter")
    root.geometry("800x600")

    # Provide the path to the uploaded Excel file
    excel_file_path = "SACE2__excel_qty_result_0121-022123.xlsx"

    # Create and pack the ExcelSheetWidget
    excel_widget = ExcelSheetWidget(root, excel_file_path)
    excel_widget.pack(fill=tk.BOTH, expand=True)

    # Start the Tkinter event loop
    root.mainloop()
