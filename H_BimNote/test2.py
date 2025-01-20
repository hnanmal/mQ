import tkinter as tk
from tksheet import Sheet


def setup_spreadsheet():
    root = tk.Tk()
    root.title("Spreadsheet Example")
    root.geometry("1200x600")

    # Create the Sheet widget
    sheet = Sheet(
        root,
        headers=[
            "Work Master Code",
            "Gauge Code",
            "Description",
            "Spec.",
            "Additional Spec.",
            "Reference to",
            "UoM",
            "Total",
            "Building Name",
            "Team Turbine Building",
            "Ram Turbine Foundation",
            "Gate House",
        ],
        header_font=("Arial", 10, "bold"),
    )
    sheet.pack(expand=True, fill="both")

    # Example Data
    data = [
        ["Earth Work", "-", "", "", "", "", "", "0.00", "", "", "", ""],
        ["", "", "", "", "", "", "", "0.00", "", "", "", ""],
        ["Pile Work", "", "", "", "", "", "", "0.00", "", "", "", ""],
        ["Piling Work", "", "", "", "", "", "", "0.00", "", "", "", ""],
    ]

    # Populate the sheet with data
    sheet.set_sheet_data(data)

    # Highlight specific rows
    sheet.highlight_cells(row=0, column=0, bg="lightgreen", fg="black")
    sheet.highlight_cells(row=2, column=0, bg="lightgreen", fg="black")

    # Disable editing for header rows
    # sheet.disable_cells(rows=[0, 2])

    # Make the sheet editable except for highlighted rows
    sheet.enable_bindings(
        ("single_select", "row_select", "column_select", "arrowkeys", "edit_cell")
    )

    root.mainloop()


if __name__ == "__main__":
    setup_spreadsheet()
