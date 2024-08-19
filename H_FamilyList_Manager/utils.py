# utils.py

import os
import tkinter as tk
from tkinter import messagebox


class FileUtils:
    @staticmethod
    def read_file(file_path):
        """Read and return the contents of a file."""
        with open(file_path, "r") as file:
            return file.read()

    @staticmethod
    def write_file(file_path, content):
        """Write content to a file."""
        with open(file_path, "w") as file:
            file.write(content)

    @staticmethod
    def file_exists(file_path):
        """Check if a file exists."""
        return os.path.exists(file_path)

    @staticmethod
    def delete_file(file_path):
        """Delete a file."""
        if FileUtils.file_exists(file_path):
            os.remove(file_path)

    @staticmethod
    def _restore_subtree(app, parent, children):
        """Recursively restore a subtree of items."""
        for child_data in children:
            child_item = app.tree.insert(
                parent,
                "end",
                text=child_data["number"],
                values=(child_data["name"], child_data["description"]),
                tags=child_data["tags"],
            )
            app.original_names[child_item] = child_data["name"]

            # Recursively restore the subtree
            FileUtils._restore_subtree(app, child_item, child_data["children"])

            # Update the displayed name with correct indentation
            app.treeview_operations.update_displayed_name(child_item)

    @staticmethod
    def undo_last_action(app):
        """Undo the last action."""
        if not app.undo_stack:
            tk.messagebox.showinfo("Undo", "Nothing to undo.")
            return

        last_action = app.undo_stack.pop()
        last_action_type = last_action["type"]

        if last_action_type == "add":
            if app.tree.exists(last_action["item"]):  # Check if item exists
                app.tree.delete(last_action["item"])

        elif last_action_type == "delete":
            parent = last_action["parent"]
            index = last_action["index"]
            item_data = last_action["data"]

            # Reinsert the item under the correct parent and at the correct index
            new_item = app.tree.insert(
                parent,
                index,
                text=item_data["number"],
                values=(item_data["name"], item_data["description"]),
                tags=item_data["tags"],  # Restore the item's styles
            )

            # Restore the original name and any other data associated with the item
            app.original_names[new_item] = item_data["name"]

            # Restore sub-elements (children)
            FileUtils._restore_subtree(app, new_item, item_data["children"])

            # Update the displayed name with correct indentation
            app.treeview_operations.update_displayed_name(new_item)

            # Optionally, expand the parent so the restored item is visible
            app.tree.item(parent, open=True)

            # Reselect the restored item
            app.tree.selection_set(new_item)

        elif last_action_type == "edit":
            item = last_action["item"]
            if app.tree.exists(item):  # Check if item exists
                original_value = last_action["original"]
                if last_action["column"] == "name":
                    app.original_names[item] = original_value
                    app.treeview_operations.update_displayed_name(item)
                elif last_action_type == "description":
                    app.tree.set(item, "description", original_value)

        elif last_action_type == "move":
            # Undo a move by restoring the item's original parent and position
            for position in last_action["original_positions"]:
                item = position["item"]
                if app.tree.exists(item):  # Check if item exists
                    original_parent = position["original_parent"]
                    original_index = position["original_index"]
                    app.tree.move(item, original_parent, original_index)
                    app.treeview_operations.renumber_children(original_parent)

        elif last_action_type == "move_down":
            # Undo moving the item down by restoring its original position
            for position in last_action["original_positions"]:
                item = position["item"]
                if app.tree.exists(item):  # Check if item exists
                    original_parent = position["original_parent"]
                    original_index = position["original_index"]
                    app.tree.move(item, original_parent, original_index)
                    app.treeview_operations.renumber_children(original_parent)

        elif last_action_type == "move_up":
            # Undo moving the item up by restoring its original position
            for position in last_action["original_positions"]:
                item = position["item"]
                if app.tree.exists(item):  # Check if item exists
                    original_parent = position["original_parent"]
                    original_index = position["original_index"]
                    app.tree.move(item, original_parent, original_index)
                    app.treeview_operations.renumber_children(original_parent)
