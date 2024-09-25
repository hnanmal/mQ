import tkinter as tk
from tksheet import Sheet


def on_combo_selected(event):
    selected_value = sheet.get_cell_data(*sheet.currently_selected())
    print(f"Selected Value: {selected_value}")


# Create the main window
root = tk.Tk()
root.title("tksheet with Combobox")
root.geometry("600x400")

# Create a Sheet widget
sheet = Sheet(root, headers=["Column A", "Column B", "Column C"], width=600, height=400)
sheet.pack(expand=True, fill="both")

# Set sheet data
data = [
    ["Row1 Col1", "", "Row1 Col3"],
    ["Row2 Col1", "Dropdown", "Row2 Col3"],
    ["Row3 Col1", "", "Row3 Col3"],
]
sheet.set_sheet_data(data)

# Enable editing and set data type for specific cells
sheet.enable_bindings(
    "single_select", "row_select", "column_select", "arrowkeys", "edit_bindings"
)

# Define dropdown options
dropdown_options = ["Option 1", "Option 2", "Option 3"]

# Set dropdown options for a specific cell
sheet.create_dropdown(
    r=1,  # Row index for dropdown cell
    c=1,  # Column index for dropdown cell
    values=dropdown_options,  # Dropdown options
    set_value=dropdown_options[0],  # Default value
    redraw=True,  # Redraw sheet to display dropdown
)

# Bind an event when selection changes
sheet.bind("<<ComboboxSelected>>", on_combo_selected)

# Start the Tkinter main loop
root.mainloop()
