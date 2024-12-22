import json
import tkinter as tk
from tksheet import Sheet


class TreeSheet:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data

        # Frame for the tksheet widget
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        # Initialize tksheet with treeview and checkbox support
        self.sheet = Sheet(
            self.frame,
            headers=["Name", "Level 1", "Level 2", "Level 3", "Enabled/Not Used"],
            treeview=True,
        )
        self.sheet.enable_bindings()  # Enable cell editing, resizing, etc.
        self.sheet.pack(fill="both", expand=True)

        # Populate the sheet with hierarchical data
        self.row_counter = 0  # Ensure unique row IDs
        self.populate_sheet()

    def populate_sheet(self):
        """Populate the tksheet in treeview mode."""
        for item in self.data:
            self.insert_item(item)

    def insert_item(self, item, parent=None):
        """Recursively insert items into the tksheet."""
        # Generate a unique ID for the row
        item_id = f"row_{self.row_counter}"
        self.row_counter += 1
        is_last_level = not any(
            isinstance(child, dict) for child in item.get("children", [])
        )

        # Insert the row
        self.sheet.insert(
            iid=item_id,
            parent=parent,
            text=item["name"],
            values=item["values"] + ([True] if is_last_level else [""]),
        )

        # Add checkboxes only for last-level rows
        if is_last_level:
            try:
                self.sheet.checkbox(item_id, checked=True)
            except Exception as e:
                print(f"Error adding checkbox for {item_id}: {e}")

        # Recursively insert child items
        for child in item.get("children", []):
            if isinstance(child, dict):
                self.insert_item(child, parent=item_id)
            else:
                # Handle leaf children (non-dict)
                leaf_id = f"row_{self.row_counter}"
                self.row_counter += 1
                self.sheet.insert(
                    iid=leaf_id,
                    parent=item_id,
                    text=child,
                    values=[child] + [""] * (len(item["values"]) - 1) + [True],
                )
                try:
                    self.sheet.checkbox(leaf_id, checked=True)
                except Exception as e:
                    print(f"Error adding checkbox for {leaf_id}: {e}")

    def toggle_checkbox(self, column="E", checked=None):
        """Toggle the checkbox value in the specified column."""
        self.sheet.click_checkbox(column, checked=checked)

    def save_data(self):
        """Save the data back into hierarchical format."""
        return (
            self.data
        )  # This would need to collect the current sheet state if edits are allowed


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    # Load the data from the file
    with open("resource/PlantArch_BIM Standard.bnote", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Extract the specific data
    data = json_data["std-GWM"]["children"]

    # Initialize and display TreeSheet
    tree_sheet = TreeSheet(root, data)

    # Add a button to save data
    save_button = tk.Button(
        root, text="Save", command=lambda: print(tree_sheet.save_data())
    )
    save_button.pack()

    # Add a button to toggle checkbox state
    toggle_button = tk.Button(
        root,
        text="Toggle Checkboxes",
        command=lambda: tree_sheet.toggle_checkbox(checked=False),
    )
    toggle_button.pack()

    root.mainloop()
