import tkinter as tk
from tksheet import Sheet
import openpyxl


class PinColumnSheetWidget(tk.Frame):
    def __init__(self, parent, excel_file, pin_columns=1, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.excel_file = excel_file
        self.pin_columns = pin_columns  # Number of columns to pin
        self.data = []
        self.column_headers = []

        # Load Excel data
        self.load_excel_data()

        # Create frames for pinned and scrollable sections
        self.pinned_frame = tk.Frame(self)
        self.pinned_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Pinned Sheet (Frozen columns)
        self.pinned_sheet = Sheet(
            self.pinned_frame,
            data=[[row[col] for col in range(self.pin_columns)] for row in self.data],
            column_width=120,
            height=400,
            width=self.pin_columns * 120,
        )
        self.pinned_sheet.enable_bindings(
            "copy",
            "rc_select",
            "row_select",
            "single_select",
        )
        self.pinned_sheet.pack(fill=tk.BOTH, expand=True)

        # Scrollable Sheet (Remaining columns)
        self.scrollable_sheet = Sheet(
            self.scrollable_frame,
            data=[
                [row[col] for col in range(self.pin_columns, len(row))]
                for row in self.data
            ],
            column_width=120,
            height=400,
            width=(len(self.data[0]) - self.pin_columns) * 120,
        )
        self.scrollable_sheet.enable_bindings(
            "copy",
            "rc_select",
            "row_select",
            "single_select",
            "scroll_y",
            "scroll_x",
        )
        self.scrollable_sheet.pack(fill=tk.BOTH, expand=True)

        # Synchronize scrolling and row heights
        self.sync_scrolling()
        self.sync_row_heights()

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

    def sync_scrolling(self):
        """Synchronize vertical scrolling between the pinned and scrollable sheets."""

        def on_scroll_y(event):
            self.pinned_sheet.yview_moveto(event.widget.yview()[0])
            self.scrollable_sheet.yview_moveto(event.widget.yview()[0])

        self.pinned_sheet.bind("<MouseWheel>", on_scroll_y)
        self.scrollable_sheet.bind("<MouseWheel>", on_scroll_y)

    def sync_row_heights(self):
        """Synchronize row heights between the pinned and scrollable sheets."""
        for row in range(len(self.data)):
            pinned_height = self.pinned_sheet.row_height(row)
            scrollable_height = self.scrollable_sheet.row_height(row)
            max_height = max(pinned_height, scrollable_height)
            self.pinned_sheet.row_height(row, max_height)
            self.scrollable_sheet.row_height(row, max_height)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Column Pinning Example")
    root.geometry("1200x600")

    # Replace with your Excel file path
    excel_file_path = "SACE2__excel_qty_result_0121-022123.xlsx"

    # Create and pack the PinColumnSheetWidget
    pin_column_widget = PinColumnSheetWidget(root, excel_file_path, pin_columns=11)
    pin_column_widget.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
