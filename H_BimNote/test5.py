import tkinter as tk
from tksheet import Sheet
import json
import uuid


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
            headers=[
                "Enabled/Not Used",
                "Name",
                "Level 1",
                "Level 2",
                "Level 3",
            ],
            treeview=True,
        )

        # self.sheet.set_options(
        #     {
        #         # "font": ["Arial Narrow", 8, "normal"],  # 데이터 셀의 글씨 설정
        #         # "header_font": ("Arial Narrow", 8, "normal"),  # 헤더 글씨 설정
        #         # "index_font": ("Arial Narrow", 8, "normal"),  # 헤더 글씨 설정
        #         "default_row_height": [
        #             50
        #         ],  # 25,  # 행 높이 설정 (글씨 크기에 맞게 조정)
        #     }
        # )
        self.sheet.set_index_width(750)
        self.sheet.set_options(index_font=("Arial Narrow", 8, "normal"))

        self.sheet.enable_bindings()  # Enable cell editing, resizing, etc.
        self.sheet.pack(fill="both", expand=True)

        # Create checkboxes in the last column
        self.sheet.checkbox("A", checked=True)

        # Populate the sheet with hierarchical data
        self.populate_sheet()

        # Automatically expand the treeview
        self.expand_treeview()

    def populate_sheet(self):
        """Populate the tksheet in treeview mode."""
        for item in self.data:
            self.insert_item(item)

    def insert_item(self, item, parent=""):
        """Recursively insert items into the tksheet."""
        # item_id = item["name"]  # Use the name as a unique ID
        item_id = item["name"] + "__" + str(uuid.uuid4())  # Use the name as a unique ID
        if len(item["values"]) == 9:
            self.sheet.insert(
                iid=item_id,
                parent=parent,
                # text=item["values"][2] + " " + item["values"][3],
                text=item["values"][3],
                values=item["values"],
            )
        else:
            self.sheet.insert(
                iid=item_id,
                parent=parent,
                text=item["name"],
                values=item[
                    "values"
                ],  # + [True],  # Add default checkbox state as True
            )
        for child in item.get("children", []):
            if isinstance(child, dict):
                self.insert_item(child, parent=item_id)
            else:
                self.sheet.insert(
                    parent=item_id,
                    iid=str(uuid.uuid4()),
                    text=child,
                    values=[child] + [""] * (len(item["values"]) - 1) + [True],
                )

    def expand_treeview(self):
        """Automatically expand all treeview nodes using tree_set_open."""
        # open_ids = self.collect_open_ids(self.data)
        # self.sheet.tree_set_open(open_ids)
        self.sheet.tree_open()

    def collect_open_ids(self, data):
        """Recursively collect all IDs for tree nodes."""
        open_ids = []
        for item in data:
            if isinstance(item, dict):
                open_ids.append(item["name"])
                open_ids.extend(self.collect_open_ids(item.get("children", [])))
        return open_ids

    def toggle_checkbox(self, column="A", checked=None):
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
    root.state("zoomed")

    # # Example hierarchical data
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
        json_data = json.load(file)

    # Extract the specific data
    data = json_data["std-familylist"]["children"][0]["children"]

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
