import tkinter as tk
from tkinter import ttk
from tksheet import Sheet

# Create the main window
root = tk.Tk()
root.title("tksheet Dropdown Example with Custom Row Count")

# Create a Sheet widget with some initial data
sheet = Sheet(
    root,
    data=[["Click to select", "", ""], ["", "", ""], ["", "", ""]],
    headers=["Column 1", "Column 2", "Column 3"],
    width=500,
    height=300,
)
sheet.pack(fill=tk.BOTH, expand=True)

# Enable bindings for basic sheet interactions
sheet.enable_bindings(
    (
        "single_select",  # Allow single cell selection
        "column_select",  # Allow column selection
        "row_select",  # Allow row selection
        "arrowkeys",  # Enable keyboard arrow keys
        "edit_cell",  # Allow editing of cells
        "rc_select",  # Enable right-click menu for cells
    )
)

# Define dropdown values
dropdown_values = [
    "Item 1",
    "Item 2",
    "Item 3",
    "Item 4",
    "Item 5",
    "Item 6",
    "Item 7",
    "Item 8",
    "Item 9",
    "Item 10",
]


# Function to open a custom dropdown with a limited number of visible rows
def open_custom_dropdown(row, column):
    # Create a Toplevel window as a popup for the dropdown
    top = tk.Toplevel(root)
    top.geometry(f"+{root.winfo_pointerx()}+{root.winfo_pointery()}")

    # Create a Combobox inside the Toplevel
    combobox = ttk.Combobox(top, values=dropdown_values, state="readonly")
    combobox.pack(padx=5, pady=5)

    # Set the height of the dropdown list (number of visible items)
    combobox["height"] = (
        8  # Adjust this number to control visible rows (e.g., 8 rows visible)
    )

    # Set focus on the Combobox
    combobox.focus_set()

    # Function to handle selection from the dropdown
    def on_select(event=None):
        selected_value = combobox.get()
        # Set the selected value back into the sheet cell
        sheet.set_cell_data(row, column, selected_value)
        # Destroy the Toplevel window after selection
        top.destroy()

    # Bind the selection event
    combobox.bind("<<ComboboxSelected>>", on_select)

    # Close the dropdown if focus is lost
    top.bind("<FocusOut>", lambda event: top.destroy())


# Bind the custom dropdown function to cell clicks
def on_cell_clicked(event):
    # Get the currently selected cell from the sheet
    selected = sheet.get_currently_selected()

    # Extract the row and column from the returned object if available
    try:
        clicked_row = selected.row
        clicked_column = selected.column

        # Check if the specific cell (0, 0) is clicked
        if clicked_row == 0 and clicked_column == 0:
            open_custom_dropdown(clicked_row, clicked_column)
    except AttributeError:
        print(f"Unexpected structure for selected value: {selected}")


# Attach the cell click binding to trigger dropdown on specific cell
sheet.extra_bindings([("cell_select", on_cell_clicked)])

# Start the Tkinter event loop
root.mainloop()
