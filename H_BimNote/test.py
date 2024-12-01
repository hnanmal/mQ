import ttkbootstrap as ttk

# Create the main application window
app = ttk.Window(themename="cosmo")
app.geometry("600x400")

# Create a Treeview with an extra column for checkboxes
tree = ttk.Treeview(app, columns=("Checkbox", "A", "B"), show="headings")
tree.heading("Checkbox", text="Select")
tree.heading("A", text="Column A")
tree.heading("B", text="Column B")
tree.pack(fill="both", expand=True, pady=10)

# Insert items with an unchecked state ('[ ]')
for i in range(5):
    tree.insert("", "end", values=("[   ]", f"Item {i + 1}", f"Value {i + 1}"))


# Function to toggle the checkbox state
def toggle_checkbox(event):
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)
    if item_id and column_id == "#1":  # If the checkbox column was clicked
        current_values = tree.item(item_id, "values")
        new_state = "[✓]" if current_values[0] == "[   ]" else "[   ]"
        tree.item(item_id, values=(new_state, current_values[1], current_values[2]))


# Bind left-click on the Treeview to toggle the checkbox
tree.bind("<Button-1>", toggle_checkbox)

# Start the main event loop
app.mainloop()
