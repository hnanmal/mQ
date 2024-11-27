from src.core.fp_utils import *
import tkinter as tk
from tkinter import ttk, simpledialog


class TreeviewEditor:
    def __init__(self, state, impl_treeview):
        self.impl_treeview = impl_treeview
        self.treeview = self.impl_treeview.treeview
        self.tree = self.treeview.tree
        self.state = state
        self.entry_widget = None
        self.current_item = None
        self.current_column = None

        # Bind double-click to initiate edit
        self.tree.bind("<Double-1>", self.on_double_click)

    def generate_id_from_values(self, values):
        """Generate an ID from the first non-empty value in the values list."""
        for value in values:
            if value:  # If value is not empty
                return value
        return "default_id"  # If no non-empty value found, provide a default ID

    def add_item(self, parent_id="", values=()):
        """Add an item to the Treeview and to the state."""
        # Generate an ID from the first non-empty value in the values list
        item_id = self.generate_id_from_values(values)

        # Insert the item into the Treeview with the custom ID
        self.tree.insert(parent_id, "end", iid=item_id, values=values)

        # Insert the item into the state with the same ID
        item_data = {"id": item_id, "values": list(values), "children": []}

        # Add to state: either as a root item or as a child
        if parent_id:
            # Find the parent in the state and add as a child
            self._add_child_to_state(
                self.state.team_std_info[self.impl_treeview.data_kind],
                parent_id,
                item_data,
            )
        else:
            # Add as a root item
            self.state.team_std_info[self.impl_treeview.data_kind].append(item_data)

    def _add_child_to_state(self, items, parent_id, child_data):
        """Recursively add a child to the correct parent in the state."""
        for item in items:
            if item["id"] == parent_id:
                item["children"].append(child_data)
                return True
            if item["children"]:
                if self._add_child_to_state(item["children"], parent_id, child_data):
                    return True
        return False

    def on_double_click(self, event):
        # Identify the column and item that was double-clicked
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not item_id or not column:
            return

        self.current_item = item_id
        self.current_column = int(column.replace("#", "")) - 1

        # Get the current value of the selected item
        current_value = self.tree.item(item_id, "values")[self.current_column]

        # Create an Entry widget for editing
        x, y, width, height = self.tree.bbox(item_id, column)
        self.entry_widget = tk.Entry(self.tree, width=width)
        self.entry_widget.place(x=x, y=y, width=width, height=height)
        self.entry_widget.insert(0, current_value)
        self.entry_widget.focus()

        # Bind events for Entry widget
        self.entry_widget.bind("<Return>", self.on_edit_complete)
        self.entry_widget.bind("<Escape>", self.on_edit_cancel)

    def on_edit_complete(self, event):
        if self.current_item is None or self.current_column is None:
            return

        # Get the updated value from the Entry widget
        new_value = self.entry_widget.get()

        # Update the Treeview item value ## 위젯 변경 말고 스테이트 변경 후 노티 방식으로
        values = list(self.tree.item(self.current_item, "values"))
        values[self.current_column] = new_value
        # self.tree.item(self.current_item, values=values)

        # Update the state with the new value
        self.update_state(self.current_item, values)
        # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
        self.state.observer_manager.notify_observers(self.state)

        # Destroy the Entry widget
        self.entry_widget.destroy()
        self.entry_widget = None

    def on_edit_cancel(self, event):
        # Cancel editing and destroy the Entry widget
        if self.entry_widget:
            self.entry_widget.destroy()
            self.entry_widget = None

    def update_state(self, item_id, new_values):
        # Recursively update the state with the new values
        def update_item_data(items):
            for item in items:
                if item["id"] == item_id:
                    item["values"] = new_values
                    return True
                if item["children"]:
                    if update_item_data(item["children"]):
                        return True
            return False

        tree_data = self.state.team_std_info[self.impl_treeview.data_kind]
        update_item_data(tree_data)
        # self.state.team_std_info[self.impl_treeview.data_kind] = tree_data
