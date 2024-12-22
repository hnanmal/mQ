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

        # Create checkboxes in the last column
        self.sheet.checkbox("E", checked=True)

        # Populate the sheet with hierarchical data
        self.populate_sheet()

        # Automatically expand the treeview
        self.expand_treeview()

    def populate_sheet(self):
        """Populate the tksheet in treeview mode."""
        for item in self.data:
            self.insert_item(item)

    # def insert_item(self, item, parent=""):
    #     """Recursively insert items into the tksheet."""
    #     item_id = item["name"]  # Use the name as a unique ID
    #     self.sheet.insert(
    #         iid=item_id,
    #         parent=parent,
    #         text=item["name"],
    #         # values=item["values"] + [],  # Add default checkbox state as True
    #     )
    #     for child in item.get("children", []):
    #         if isinstance(child, dict):
    #             self.insert_item(child, parent=item_id)
    #         else:
    #             self.sheet.insert(
    #                 parent=item_id,
    #                 iid=child,
    #                 text=child,
    #                 # values=[child] + [""] * (len(item["values"]) - 1) + [True],
    #                 values=[child] + [""] * (len(item["values"]) - 1) + [""],
    #             )


def insert_item(self, item, parent="", path=""):
    """Recursively insert items into the tksheet."""
    # Generate a unique ID based on the current path
    item_id = f"{path}/{item['name']}".replace(" ", "_")  # Ensure no spaces in ID
    is_last_level = not any(
        isinstance(child, dict) for child in item.get("children", [])
    )

    # Insert the row
    self.sheet.insert(
        iid=item_id,
        parent=parent,
        text=item["name"],
        values=item["values"]
        + ([True] if is_last_level else [""]),  # Checkbox only for last level
    )

    # Add checkboxes only for last-level rows
    if is_last_level:
        self.sheet.checkbox(f"{item_id} E", checked=True)

    for i, child in enumerate(item.get("children", [])):
        if isinstance(child, dict):
            # Pass the current path to children for unique ID generation
            self.insert_item(child, parent=item_id, path=f"{path}/{item['name']}_{i}")
        else:
            child_id = f"{item_id}_child_{i}"  # Unique ID for string children
            self.sheet.insert(
                parent=item_id,
                iid=child_id,
                text=child,
                values=[child] + [""] * (len(item["values"]) - 1) + [True],
            )
            self.sheet.checkbox(
                f"{child_id} E", checked=True
            )  # Checkbox for string children

    def expand_treeview(self):
        """Automatically expand all treeview nodes using tree_set_open."""
        open_ids = self.collect_open_ids(self.data)
        self.sheet.tree_set_open(open_ids)

    def collect_open_ids(self, data):
        """Recursively collect all IDs for tree nodes."""
        open_ids = []
        for item in data:
            if isinstance(item, dict):
                open_ids.append(item["name"])
                open_ids.extend(self.collect_open_ids(item.get("children", [])))
        return open_ids

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

    # Example hierarchical data
    # data = [
    #     {
    #         "name": "Earth Work",
    #         "values": ["Earth Work", "", "", ""],
    #         "children": [
    #             {
    #                 "name": "EARTH",
    #                 "values": ["", "EARTH", "", ""],
    #                 "children": [
    #                     {
    #                         "name": "Excavation_A",
    #                         "values": ["", "", "Excavation_A", ""],
    #                         "children": [
    #                             "A01ZZ001-00010 | AR | A01 | Earth Work | ZZ | - | 001 | Excavation | 01 | Soil, Manual | 07 | Manual Excavation Above GWL | M3 | M3 | A01ZZ001 | A01ZZ001-00010",
    #                             "A01ZZ001-00011 | AR | A01 | Earth Work | ZZ | - | 001 | Excavation | 01 | Soil, Manual | 08 | Manual Excavation Below GWL | M3 | M3 | A01ZZ001 | A01ZZ001-00011",
    #                         ],
    #                     },
    #                     {
    #                         "name": "Backfilling_A",
    #                         "values": ["", "", "Backfilling_A", ""],
    #                         "children": [
    #                             "A01ZZ003-00001 | AR | A01 | Earth Work | ZZ | - | 003 | Backfill | 06 | Re-use, Soil | Compaction=(  )% | M3 | M3 | A01ZZ003 | A01ZZ003-00001"
    #                         ],
    #                     },
    #                 ],
    #             }
    #         ],
    #     }
    # ]
    with open("resource/PlantArch_BIM Standard.bnote", "r", encoding="utf-8") as file:
        data_ = json.load(file)

    data = data_["std-GWM"]["children"]

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
