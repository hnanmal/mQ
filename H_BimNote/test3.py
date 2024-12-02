import tkinter as tk
from tkinter import ttk

# Create the main application window
app = tk.Tk()
app.title("Treeview with Dropdown Simulation")
app.geometry("700x400")

# Create a Treeview widget
columns = ("A", "B", "C")
tree = ttk.Treeview(app, columns=columns, show="headings")
tree.heading("A", text="Column A")
tree.heading("B", text="Column B (Dropdown)")
tree.heading("C", text="Column C")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Insert some sample data into the Treeview
for i in range(5):
    tree.insert(
        "", "end", values=(f"Item {i+1} - A", f"Item {i+1} - B", f"Item {i+1} - C")
    )


# Function to handle double-click event and create a dropdown
def on_double_click(event):
    # Identify which row and column was clicked
    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    # Only create a Combobox for specific column (e.g., column B)
    if column_id == "#2" and row_id:
        # Get the bounding box of the clicked cell
        x, y, width, height = tree.bbox(row_id, column_id)

        # Get current value
        current_value = tree.set(row_id, column_id)

        # Create Combobox
        combobox = ttk.Combobox(app, values=["Option 1", "Option 2", "Option 3"])
        combobox.place(
            x=x + tree.winfo_x(), y=y + tree.winfo_y(), width=width, height=height
        )
        combobox.set(current_value)
        combobox.focus()

        # Function to handle value selection
        def save_selection(event):
            new_value = combobox.get()
            tree.set(row_id, column_id, new_value)
            combobox.destroy()

        # Bind selection to Combobox
        combobox.bind("<<ComboboxSelected>>", save_selection)
        combobox.bind("<FocusOut>", lambda e: combobox.destroy())


# Bind double-click to show the dropdown
tree.bind("<Double-1>", on_double_click)

# Run the main event loop
app.mainloop()
