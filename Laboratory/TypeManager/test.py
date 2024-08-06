import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Create a style
style = ttk.Style()
style.configure("Custom.Treeview", rowheight=25)  # Set row height
style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))

# Configure tag for the light green background
style.map(
    "Custom.Treeview",
    background=[("selected", "blue")],  # Selected row color
    foreground=[("selected", "white")],
)

# Set the Treeview widget's style
tree = ttk.Treeview(root, style="Custom.Treeview", columns=("name", "description"))
tree.heading("#0", text="#")
tree.heading("name", text="Item")
tree.heading("description", text="Description")

# Add sample items with different colors for demonstration
for i in range(5):
    item_id = tree.insert(
        "", "end", text=str(i), values=(f"Item {i}", f"Description {i}")
    )
    if i % 2 == 0:
        tree.item(item_id, tags=("light_green",))
    else:
        tree.item(item_id, tags=("default",))

# Set tag styles for alternating rows
tree.tag_configure("light_green", background="#ccffcc")
tree.tag_configure("default", background="white")

tree.pack(expand=True, fill="both")
root.mainloop()
