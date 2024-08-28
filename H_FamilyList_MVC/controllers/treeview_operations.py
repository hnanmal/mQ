# Version: 1.0.9

import tkinter as tk
from tkinter import ttk
from collections import OrderedDict

from controllers.main_controller import (
    on_item_double_click,
    on_item_single_click,
    update_center_title_label,
)


class TreeviewOperations:
    def __init__(self, app):
        self.app = app

        # Configure the treeview styles after treeview is fully initialized
        self.configure_styles()

        # app.tree.bind(
        # self.app.bind(
        #     "<Button-3>",
        #     self.app.context_menu_manager.show_context_menu,
        # )

    def configure_styles(self):
        # Create a style for the Treeview to ensure custom tag colors are applied
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
        # tags = ("default",) <- 인덴트 오류 발생 시킴
        tags = ()

        if top_level:
            tags = ("top_level",)
        elif depth == 4:
            tags = ("level_4",)

        item_id = self.app.tree.insert(
            parent, "end", text=number, values=(original_name, description), tags=tags
        )
        self.app.original_names[item_id] = original_name
        self.update_displayed_name(item_id)

        if track_undo:
            # Push this add action to the undo stack if tracking is enabled
            self.app.undo_stack.append(
                {"type": "add", "item": item_id, "parent": parent}
            )

        # # Push this add action to the undo stack
        # self.app.undo_stack.append({"type": "add", "item": item_id})

        return item_id

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

    def renumber_children(self, parent):
        children = self.app.tree.get_children(parent)
        for i, child in enumerate(children, start=1):
            parent_number = self.app.tree.item(parent, "text")
            new_number = f"{parent_number}.{i}"
            self.app.tree.item(child, text=new_number)
            self.update_displayed_name(child)
            self.renumber_children(child)

    def reapply_styles(self, item):
        """Force reapply of styles to the given item."""
        tags = self.app.tree.item(item, "tags")
        for tag in tags:
            self.app.tree.tag_configure(tag)
        self.app.tree.update_idletasks()  # Ensure the display is updated

    def add_item(self):
        selected_item = self.app.tree.focus()
        if not selected_item:
            new_index = len(self.app.tree.get_children())
            new_item_id = self.add_numbered_item(
                "", str(new_index), "New Top-level Item", "", top_level=True
            )
            self.app.tree.selection_set(new_item_id)
        else:
            parent_number = self.app.tree.item(selected_item, "text")
            children = self.app.tree.get_children(selected_item)
            new_index = len(children) + 1
            new_number = f"{parent_number}.{new_index}"
            new_item_id = self.add_numbered_item(
                selected_item, new_number, "New Sub-item", ""
            )
            self.app.tree.selection_set(new_item_id)
            self.app.tree.item(selected_item, open=True)
            # print(dir(new_item_id))

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
                "children": self._get_subtree(item),  # Get the entire subtree
            }

            # Log the action for debugging
            print(f"Adding delete action to undo stack for item {item_data['number']}")

            # Push the delete operation to the undo stack
            self.app.undo_stack.append(
                {
                    "type": "delete",
                    "item": item,
                    "parent": parent,
                    "index": index,
                    "data": item_data,
                }
            )

            # Proceed with deletion
            self.app.tree.delete(item)
            self.app.original_names.pop(item, None)

        for parent in parents_to_renumber:
            self.renumber_children(parent)

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

    def collapse_all(self):
        for item in self.app.tree.get_children():
            self.app.tree.item(item, open=False)
            self._collapse_recursive(item)

    def _collapse_recursive(self, item):
        for child in self.app.tree.get_children(item):
            self.app.tree.item(child, open=False)
            self._collapse_recursive(child)

    # def on_item_single_click(self, event):
    #     selected_item = self.app.tree.identify_row(event.y)
    #     column = self.app.tree.identify_column(event.x)
    #     if column == "#2":  # "#2" corresponds to the Description column
    #         self.edit_description(selected_item)

    # def on_item_double_click(self, event):
    #     selected_item = self.app.tree.identify_row(event.y)
    #     column = self.app.tree.identify_column(event.x)
    #     if column == "#1":
    #         self.edit_item_name(selected_item)

    def edit_item_name(self, item):
        current_value = self.app.original_names.get(item, "")

        self.app.is_text_editing = True

        entry = ttk.Entry(self.app.tree, width=len(current_value) + 5)
        entry.insert(0, current_value)
        entry.bind("<Return>", lambda e: self.save_item_name(entry, item))
        entry.bind("<FocusOut>", lambda e: self.save_item_name(entry, item))
        bbox = self.app.tree.bbox(item, column="indented_name")
        # bbox = self.app.tree.bbox(item, column="#1")
        if bbox:
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
            entry.focus()
        else:
            entry.destroy()

    def save_item_name(self, entry, item):
        try:
            new_value = entry.get()
            self.app.original_names[item] = new_value
            self.update_displayed_name(item)
        except tk.TclError:
            pass
        finally:
            self.app.is_text_editing = False  # Clear editing mode flag
            entry.destroy()

    def edit_description(self, item):
        current_value = self.app.tree.set(item, "description")

        # Set editing mode flag
        self.app.is_text_editing = True

        entry = ttk.Entry(self.app.tree, width=len(current_value) + 5)
        entry.insert(0, current_value)
        entry.bind("<Return>", lambda e: self.save_description(entry, item))
        entry.bind("<FocusOut>", lambda e: self.save_description(entry, item))
        bbox = self.app.tree.bbox(item, column="description")
        if bbox:
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
            entry.focus()
        else:
            entry.destroy()

    def save_description(self, entry, item):
        try:
            new_value = entry.get()
            self.app.tree.set(item, "description", new_value)
        except tk.TclError:
            pass
        finally:
            self.app.is_text_editing = False  # Clear editing mode flag
            entry.destroy()

    def update_level_limit(self, event):
        new_level_limit = int(self.app.level_limit_var.get())

        if new_level_limit < self.app.previous_level_limit:
            self.collapse_all_to_level(new_level_limit)

        for item in self.app.tree.get_children():
            self.app.tree.item(item, open=True)
            self._expand_recursive(item, current_level=1, level_limit=new_level_limit)

        self.app.previous_level_limit = new_level_limit

    def collapse_all_to_level(self, level_limit):
        for item in self.app.tree.get_children():
            self._collapse_to_level_recursive(
                item, current_level=1, level_limit=level_limit
            )

    def _collapse_to_level_recursive(self, item, current_level, level_limit):
        if current_level >= level_limit:
            for child in self.app.tree.get_children(item):
                self.app.tree.item(child, open=False)
        else:
            for child in self.app.tree.get_children(item):
                self._collapse_to_level_recursive(
                    child, current_level=current_level + 1, level_limit=level_limit
                )

    def _expand_recursive(self, item, current_level, level_limit):
        if current_level >= level_limit:
            return
        for child in self.app.tree.get_children(item):
            self.app.tree.item(child, open=True)
            self._expand_recursive(
                child, current_level=current_level + 1, level_limit=level_limit
            )

    # treeview_operations.py

    def collect_level_6_items(self):
        """Collect all unique level 6 items by their original name, keeping the first occurrence."""
        level_6_items = OrderedDict()  # Use OrderedDict to keep order and uniqueness
        for item in self.app.tree.get_children():
            self._collect_level_6_recursive(item, level_6_items)
        return list(
            level_6_items.keys()
        )  # Return only the names, not the entire dictionary

    def _collect_level_6_recursive(self, parent, level_6_items):
        """Recursively collect level 6 items."""
        for item in self.app.tree.get_children(parent):
            if self.get_item_depth(item) == 6:
                # Retrieve the original name without indentation
                item_name = self.app.original_names.get(item, "")
                if (
                    item_name not in level_6_items
                ):  # Add only if it's not already in the OrderedDict
                    level_6_items[item_name] = (
                        None  # Value is irrelevant, we're using keys to ensure uniqueness
                    )
            self._collect_level_6_recursive(item, level_6_items)
