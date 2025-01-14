from tksheet import Sheet
import tkinter as tk

# Tkinter main window
root = tk.Tk()
root.title("tksheet Example with Checkboxes")

# Sample data
data = [
    ["", "Row1-Col2", "Row1-Col3"],
    ["", "Row2-Col2", "Row2-Col3"],
    ["", "Row3-Col2", "Row3-Col3"],
]

# Create the sheet
sheet = Sheet(root, data=data, headers=["Checkbox", "Column2", "Column3"])
sheet.pack(expand=True, fill="both")

# Add checkboxes to all rows in column 0 (Checkbox)
checkbox_rows = [0, 1, 2]  # Rows to add checkboxes
for row in checkbox_rows:
    sheet.create_checkbox(row=row, column=0)


# Function to delete checkboxes in specific rows
def delete_checkboxes(rows_to_remove):
    for row in rows_to_remove:
        try:
            sheet.delete_checkbox(row=row, column=0)  # Remove checkbox
            print(f"Checkbox removed from row {row}")
        except Exception as e:
            print(f"Error removing checkbox from row {row}: {e}")


# Button to delete checkboxes from specific rows
tk.Button(
    root,
    text="Delete Checkboxes from Rows 1 and 3",
    command=lambda: delete_checkboxes([0, 2]),  # Specify rows to remove checkboxes
).pack()

root.mainloop()
