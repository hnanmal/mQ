import tkinter as tk
from tksheet import Sheet

# Create main window
root = tk.Tk()
root.title("Dynamic Dropdowns in tksheet")

# Sample dropdown data
first_cell_dropdown_options = ["Fruit", "Vegetable", "Drink"]
second_cell_dropdown_options = {
    "Fruit": ["Apple", "Banana", "Orange"],
    "Vegetable": ["Carrot", "Broccoli", "Spinach"],
    "Drink": ["Water", "Juice", "Soda"],
}

# Create tksheet widget
sheet = Sheet(root, headers=["Category", "Item"], height=150, width=400)
sheet.grid(row=0, column=0)

sheet.enable_bindings()

# Initial data (with empty second column)
sheet_data = [["", ""], ["", ""], ["", ""]]
sheet.set_sheet_data(sheet_data)

# Set dropdown for the first cell in the top row (A1)
sheet.create_dropdown(0, 0, values=first_cell_dropdown_options)


# Function to update the second cell dropdown (B1) based on the first cell selection
def update_second_cell_dropdown(event=None):
    selected_value = sheet.get_cell_data(0, 0)  # Get selected value from the first cell
    if selected_value in second_cell_dropdown_options:
        # Set the second cell's dropdown based on the first cell's value
        sheet.create_dropdown(0, 1, values=second_cell_dropdown_options[selected_value])
        # Optionally clear the value of the second cell when updating the dropdown
        sheet.set_cell_data(0, 1, "")


# Bind event to detect changes in the first cell (A1) and update the second cell
sheet.extra_bindings([("cell_select", update_second_cell_dropdown)])

# Start the main loop
root.mainloop()
