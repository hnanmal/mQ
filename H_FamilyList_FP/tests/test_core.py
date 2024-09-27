import tkinter as tk
from tkinter import ttk

from src.tabs.familyType_manage_tab.checkListbox import SelectableListboxWithCheckboxes


def toggle_check(item_id):
    # Toggle the checkbox state
    if treeview.item(item_id, "tags") == ("checked",):
        treeview.item(item_id, tags=("unchecked",))
    else:
        treeview.item(item_id, tags=("checked",))
    update_item_text(item_id)


def update_item_text(item_id):
    # Update the item text based on the checkbox state
    if treeview.item(item_id, "tags") == ("checked",):
        treeview.item(item_id, text=f"[x] {treeview.item(item_id, 'text')[4:]}")
    else:
        treeview.item(item_id, text=f"[ ] {treeview.item(item_id, 'text')[4:]}")


# Create the main window
root = tk.Tk()
root.title("Treeview with Checkboxes")

# Setup Treeview
treeview = ttk.Treeview(root, columns=("Item",), show="tree")
treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Define the tags for checked/unchecked
treeview.tag_configure("checked", background="lightgreen")
treeview.tag_configure("unchecked", background="white")

# Add items with checkbox-like labels
items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
for item in items:
    item_id = treeview.insert("", "end", text=f"[ ] {item}", tags=("unchecked",))
    treeview.bind("<Button-1>", lambda e, id=item_id: toggle_check(id))

d = SelectableListboxWithCheckboxes()

# Run the application
root.mainloop()
