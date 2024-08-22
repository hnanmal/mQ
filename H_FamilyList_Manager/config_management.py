# Version: 1.0.0

import json
from tkinter import simpledialog, ttk
from dialogs import ColumnSelectionDialog
from tkinter import filedialog


class ConfigurationManager:
    def __init__(self, app):
        self.app = app

    def ask_target_column(self):
        dialog = ColumnSelectionDialog(self.app)
        return dialog.result

    def save_configuration(self):
        tree_data = []
        for item in self.app.tree.get_children():
            tree_data.append(self.get_item_data(item))
        # Save to JSON file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(tree_data, f, indent=4, ensure_ascii=False)

    def load_configuration(self, file_path):
        if not file_path:
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                tree_data = json.load(f)
            # Clear existing tree
            for item in self.app.tree.get_children():
                self.app.tree.delete(item)
            # Load new tree
            for item_data in tree_data:
                self.insert_item_data("", item_data)

        # After populating the treeview, collect level 6 items
        level_6_items = self.app.treeview_operations.collect_level_6_items()

        # Update the Listbox in the "WM 그룹별 매칭" tab
        self.app.update_wm_group_matching_treeview(level_6_items)

    def get_item_data(self, item):
        item_data = {
            "number": self.app.tree.item(item, "text"),
            "name": self.app.original_names.get(
                item, ""
            ),  # Retrieve the original name from storage
            "description": self.app.tree.set(item, "description"),
            "children": [
                self.get_item_data(child) for child in self.app.tree.get_children(item)
            ],
        }
        return item_data

    def insert_item_data(self, parent, item_data):
        depth = self.app.treeview_operations.get_item_depth(parent) + 1
        tags = ("top_level",) if parent == "" else ()
        if depth == 4:
            tags = ("level_4",)
        new_item = self.app.tree.insert(
            parent,
            "end",
            text=item_data["number"],
            values=(item_data["name"], item_data["description"]),
            tags=tags,
        )
        self.app.original_names[new_item] = item_data[
            "name"
        ]  # Store original name internally
        self.app.treeview_operations.update_displayed_name(new_item)
        for child_data in item_data["children"]:
            self.insert_item_data(new_item, child_data)
