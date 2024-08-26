import json
from tkinter import filedialog


class ConfigurationManager:
    def __init__(self, app):
        self.app = app

    def load_configuration(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            # Clear the current treeview content
            self.app.tree.delete(*self.app.tree.get_children())

            # Recursively insert items into the treeview
            def insert_items(parent, items):
                for item in items:
                    item_id = self.app.treeview_operations.add_numbered_item(
                        parent,
                        item["number"],
                        item["name"],
                        item.get("description", ""),
                        top_level=(parent == ""),
                    )
                    # Recursively add children if they exist
                    if "children" in item:
                        insert_items(item_id, item["children"])
                    # Reapply styles after loading
                    self.app.treeview_operations.reapply_styles(item_id)

            insert_items("", config_data)

        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}.")

    def save_configuration(self, file_path):
        try:

            def retrieve_items(parent):
                items = []
                for item in self.app.tree.get_children(parent):
                    item_data = {
                        "number": self.app.tree.item(item, "text"),
                        "name": self.app.tree.set(item, "indented_name"),
                        "description": self.app.tree.set(item, "description"),
                        "children": retrieve_items(item),
                    }
                    items.append(item_data)
                return items

            # Retrieve all items starting from the root
            config_data = {"items": retrieve_items("")}

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"An error occurred while saving: {e}")

    def load_default_configuration(self, default_file_path):
        """Load the default configuration."""
        # default_file_path = default_file_path
        self.load_configuration(default_file_path)

    def expand_all_items(self):
        """Expand all items in the tree view."""
        for item in self.app.tree.get_children():
            self.app.tree.item(item, open=True)
            self._expand_recursive(item)

    def _expand_recursive(self, item):
        """Helper method to recursively expand all items."""
        for child in self.app.tree.get_children(item):
            self.app.tree.item(child, open=True)
            self._expand_recursive(child)
