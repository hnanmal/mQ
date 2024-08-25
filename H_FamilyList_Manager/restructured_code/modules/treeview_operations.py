import tkinter as tk
from tkinter import ttk, font

class TreeviewOperations:
    def __init__(self, app):
        self.app = app
        self.configure_styles()
        self.undo_stack = []

    def on_item_double_click(self, event):
        # Logic for handling double-click on a treeview item
        selected_item = self.app.tree.selection()
        if selected_item:
            item_text = self.app.tree.item(selected_item, "text")
            tk.messagebox.showinfo("Item Double-Clicked", f"You double-clicked on: {item_text}")
    
    def on_item_single_click(self, event):
        selected_item = self.app.tree.selection()
        if selected_item:
            item_text = self.app.tree.item(selected_item, "text")
            print(f"Item clicked: {item_text}")

    def configure_styles(self):
        # Configure the styles for the treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.map(
            "Treeview",
            background=[("selected", "blue")],
            foreground=[("selected", "white")],
        )

        # Ensure that the Treeview uses this style
        self.app.tree.configure(style="Treeview")

        # Define custom fonts
        self.font_level_0 = tk.font.Font(family="Arial", size=12, weight="bold")
        self.font_level_4 = tk.font.Font(family="Arial", size=11)
        self.default_font = tk.font.Font(family="Arial", size=9)

        # Define tag for top-level items with light green background and bold font
        self.app.tree.tag_configure(
            "top_level", background="light green", font=self.font_level_0
        )
        # Define tag for level 4 items with blue foreground and custom font
        self.app.tree.tag_configure(
            "level_4", foreground="blue", font=self.font_level_4
        )
        # Define default tag for other items
        self.app.tree.tag_configure("default", font=self.default_font)

    def reapply_styles(self, item):
        """Force reapply of styles to the given item."""
        tags = self.app.tree.item(item, "tags")
        for tag in tags:
            self.app.tree.tag_configure(tag)
        self.app.tree.update_idletasks()  # Ensure the display is updated

    def add_item(self):
        selected_item = self.app.tree.focus()
        if not selected_item:
            # If no item is selected, add as a top-level item
            new_index = len(self.app.tree.get_children()) + 1
            new_item_id = self.add_numbered_item(
                "", new_index, "New Top-level Item", "", top_level=True
            )
            self.app.tree.selection_set(new_item_id)
        else:
            # If an item is selected, add as a child of the selected item
            parent_number = self.app.tree.item(selected_item, "text")
            children = self.app.tree.get_children(selected_item)
            new_index = len(children) + 1
            new_number = f"{parent_number}.{new_index}"
            new_item_id = self.add_numbered_item(
                selected_item, new_number, "New Sub-item", ""
            )
            self.app.tree.selection_set(new_item_id)
            self.app.tree.item(selected_item, open=True)

    def add_numbered_item(
        self,
        parent,
        number,
        original_name,
        description,
        top_level=False,
        track_undo=True,
    ):
        """Add a numbered item to the treeview and optionally track it for undo."""
        depth = self.get_item_depth(parent) + 1
        
        # Assign default tags
        tags = ("default",)

        # Set specific tags based on conditions
        if top_level:
            tags = ("top_level",)
        elif depth == 4:
            tags = ("level_4",)

        # Insert the item into the treeview with the specified tags
        item_id = self.app.tree.insert(
            parent, "end", text=number, values=(original_name, description), tags=tags
        )
        self.app.original_names[item_id] = original_name
        self.update_displayed_name(item_id)

        if track_undo:
            # Push this add action to the undo stack if tracking is enabled
            action = {"type": "add", "item": item_id, "parent": parent}
            self.undo_stack.append(action)
            print(f"[DEBUG] Added to undo stack: {action}")

        return item_id


    def remove_selected_item(self):
        selected_items = self.app.tree.selection()
        if not selected_items:
            return

        parents_to_renumber = set()
        for item in selected_items:
            parent = self.app.tree.parent(item)
            if parent:
                parents_to_renumber.add(parent)

            # Capture the item's data, styles, and children before deleting
            index = self.app.tree.index(item)
            item_data = {
                "number": self.app.tree.item(item, "text"),
                "name": self.app.original_names.get(item, ""),
                "description": self.app.tree.set(item, "description"),
                "tags": self.app.tree.item(item, "tags"),
                "children": self._get_subtree(item),
            }

            # Log the action for debugging
            print(f"[DEBUG] Adding delete action to undo stack for item {item_data['number']}")

            # Push the delete operation to the undo stack
            action = {
                "type": "delete",
                "item": item,
                "parent": parent,
                "index": index,
                "data": item_data,
            }
            self.undo_stack.append(action)

            # Proceed with deletion
            self.app.tree.delete(item)
            self.app.original_names.pop(item, None)

        for parent in parents_to_renumber:
            self.renumber_children(parent)

    def renumber_children(self, parent):
        children = self.app.tree.get_children(parent)
        for i, child in enumerate(children, start=1):
            parent_number = self.app.tree.item(parent, "text")
            new_number = f"{parent_number}.{i}"
            self.app.tree.item(child, text=new_number)
            self.update_displayed_name(child)
            self.renumber_children(child)

    def update_displayed_name(self, item_id):
        original_name = self.app.original_names.get(item_id, "")
        depth = self.get_item_depth(item_id)
        indented_name = " " * (depth * 4) + original_name
        self.app.tree.set(item_id, "indented_name", indented_name)
        return indented_name

    def get_item_depth(self, item):
        depth = 0
        parent = self.app.tree.parent(item)
        while parent:
            depth += 1
            parent = self.app.tree.parent(parent)
        return depth

    def _get_subtree(self, item):
        children = []
        for child in self.app.tree.get_children(item):
            child_data = {
                "item": child,
                "number": self.app.tree.item(child, "text"),
                "name": self.app.original_names.get(child, ""),
                "description": self.app.tree.set(child, "description"),
                "tags": self.app.tree.item(child, "tags"),
                "children": self._get_subtree(child),
            }
            children.append(child_data)
        return children

    def collapse_all(self):
        """Collapse all items in the Treeview."""
        for item in self.app.tree.get_children():
            self.app.tree.item(item, open=False)
            self._collapse_recursive(item)

    def _collapse_recursive(self, item):
        """Recursively collapse all children of the given item."""
        for child in self.app.tree.get_children(item):
            self.app.tree.item(child, open=False)
            self._collapse_recursive(child)
    def update_level_limit(self, event=None):
        """Update the visibility of treeview items based on the selected level limit."""
        new_level_limit = int(self.app.level_limit_var.get())

        if new_level_limit < self.app.previous_level_limit:
            self.collapse_all_to_level(new_level_limit)

        for item in self.app.tree.get_children():
            self.app.tree.item(item, open=True)
            self._expand_recursive(item, current_level=1, level_limit=new_level_limit)

        self.app.previous_level_limit = new_level_limit

    def collapse_all_to_level(self, level_limit):
        """Collapse all items in the treeview down to a specific level."""
        for item in self.app.tree.get_children():
            self._collapse_to_level_recursive(
                item, current_level=1, level_limit=level_limit
            )

    def _collapse_to_level_recursive(self, item, current_level, level_limit):
        """Recursively collapse items beyond the specified level."""
        if current_level >= level_limit:
            for child in self.app.tree.get_children(item):
                self.app.tree.item(child, open=False)
        else:
            for child in self.app.tree.get_children(item):
                self._collapse_to_level_recursive(
                    child, current_level=current_level + 1, level_limit=level_limit
                )

    def _expand_recursive(self, item, current_level, level_limit):
        """Recursively expand items up to the specified level."""
        if current_level >= level_limit:
            return
        for child in self.app.tree.get_children(item):
            self.app.tree.item(child, open=True)
            self._expand_recursive(
                child, current_level=current_level + 1, level_limit=level_limit
            )

    def undo(self):
        """Undo the last operation."""
        if not self.undo_stack:
            print("[DEBUG] Undo stack is empty, nothing to undo.")
            return

        last_action = self.undo_stack.pop()
        print(f"[DEBUG] Undoing last action: {last_action}")

        if last_action["type"] == "add":
            self.app.tree.delete(last_action["item"])
        elif last_action["type"] == "delete":
            self._restore_subtree(last_action["parent"], last_action["data"])

    def _restore_subtree(self, parent, item_data):
        """Recursively restore a deleted subtree."""
        item_id = self.app.tree.insert(
            parent,
            "end",
            text=item_data["number"],
            values=(item_data["name"], item_data["description"]),
            tags=item_data["tags"],
        )
        for child in item_data["children"]:
            self._restore_subtree(item_id, child)

        print(f"[DEBUG] Restored item: {item_data['number']} with ID: {item_id}")

    def _get_subtree(self, item):
        """Recursively get all child items and their data."""
        children = []
        for child in self.app.tree.get_children(item):
            child_data = {
                "item": child,
                "number": self.app.tree.item(child, "text"),
                "name": self.app.original_names.get(child, ""),
                "description": self.app.tree.set(child, "description"),
                "tags": self.app.tree.item(child, "tags"),
                "children": self._get_subtree(child),  # Recursively get subtree
            }
            children.append(child_data)
        return children