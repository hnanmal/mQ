# models/configuration.py

import json
from tkinter import filedialog
from dialogs import ColumnSelectionDialog


class ConfigurationManager:
    def __init__(self, app):
        pass

    def ask_target_column(self, app):
        dialog = ColumnSelectionDialog(app)
        return dialog.result

    def get_item_data(self, app, item):
        item_data = {
            "number": app.tree.item(item, "text"),
            "name": app.original_names.get(
                item, ""
            ),  # Retrieve the original name from storage
            "description": app.tree.set(item, "description"),
            "children": [
                self.get_item_data(app, child) for child in app.tree.get_children(item)
            ],
        }
        return item_data

    def insert_item_data(self, app, parent, item_data):
        depth = app.treeview_operations.get_item_depth(parent) + 1
        tags = ("top_level",) if parent == "" else ()
        if depth == 4:
            tags = ("level_4",)
        new_item = app.tree.insert(
            parent,
            "end",
            text=item_data["number"],
            values=(item_data["name"], item_data["description"]),
            tags=tags,
        )
        app.original_names[new_item] = item_data[
            "name"
        ]  # Store original name internally
        app.treeview_operations.update_displayed_name(new_item)
        for child_data in item_data["children"]:
            self.insert_item_data(app, new_item, child_data)
