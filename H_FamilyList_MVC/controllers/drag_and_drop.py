# Version: 1.0.9
import tkinter as tk
from tkinter import messagebox

# import keyboard


class DragAndDropManager:
    def __init__(self, app):
        self.app = app
        self.drag_data = {"x": 0, "y": 0, "items": []}

    # Track if ctrl_space is pressed

    def ctrl_space_pressed(self, event):
        self.toggle_order_adjustment_mode()

    # Bind Alt key for temporary Order Adjustment Mode

    def toggle_order_adjustment_mode(self):
        self.app.order_adjustment_mode.set(not self.app.order_adjustment_mode.get())

        mode_text = "ON" if self.app.order_adjustment_mode.get() else "OFF"

        self.app.order_adjustment_button.config(
            text=f"Order Adjustment Mode: {mode_text}"
        )

        if self.app.order_adjustment_mode.get():
            self.app.tree.bind("<ButtonPress-1>", self.on_drag_start)
            self.app.tree.bind("<B1-Motion>", self.on_drag_motion)
            self.app.tree.bind("<ButtonRelease-1>", self.on_drag_release)
        else:
            self.app.tree.unbind("<ButtonPress-1>")
            self.app.tree.unbind("<B1-Motion>")
            self.app.tree.unbind("<ButtonRelease-1>")

    def on_drag_start(self, event):
        if not self.app.order_adjustment_mode.get() and not self.app.alt_key_down:
            return
        items = self.app.tree.selection()
        if items:
            self.drag_data["items"] = items
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            # Track original parent and index for undo
            self.drag_data["original_positions"] = []
            for item in items:
                original_parent = self.app.tree.parent(item)
                original_index = self.app.tree.index(item)
                self.drag_data["original_positions"].append(
                    {
                        "item": item,
                        "original_parent": original_parent,
                        "original_index": original_index,
                    }
                )

    def on_drag_motion(self, event):
        # if not self.app.order_adjustment_mode.get() and not self.app.alt_key_down:
        if not self.app.order_adjustment_mode.get():
            return
        if self.drag_data["items"]:
            for item in self.drag_data["items"]:
                self.app.tree.selection_set(item)
            self.app.tree.focus(self.drag_data["items"][0])

    def on_drag_release(self, event):
        # if not self.app.order_adjustment_mode.get() and not self.app.alt_key_down:
        if not self.app.order_adjustment_mode.get():
            return
        if not self.drag_data["items"]:
            return

        target_item = self.app.tree.identify_row(event.y)
        if not target_item or target_item in self.drag_data["items"]:
            self.drag_data = {"x": 0, "y": 0, "items": []}
            return

        if messagebox.askyesno(
            "Confirm Move", "Do you want to move the selected items here?"
        ):
            self.app.drag_and_drop_manager.move_items(
                self.drag_data["items"], target_item
            )

        # Ensure all UI updates are complete before removing selection
        self.app.update_idletasks()

        # Clear the selection after moving
        self.app.tree.selection_remove(self.app.tree.selection())
        self.drag_data = {"x": 0, "y": 0, "items": []}

    def move_items(self, items, target_item):
        target_parent = self.app.tree.parent(target_item)
        target_index = self.app.tree.index(target_item)

        # Capture current positions for undo
        new_positions = []
        for item in items:
            new_positions.append(
                {"item": item, "new_parent": target_parent, "new_index": target_index}
            )

        for item in items:
            parent = self.app.tree.parent(item)
            if parent == target_parent:
                # Same level move within the same parent
                self.app.tree.move(item, target_parent, target_index)
            else:
                # Move to a different level
                if self.app.treeview_operations.get_item_depth(
                    item
                ) == self.app.treeview_operations.get_item_depth(target_item):
                    self.app.tree.move(item, target_parent, target_index)
                else:
                    # Move to the end of the target parent
                    self.app.tree.move(item, target_item, "end")

            self.app.treeview_operations.renumber_children(parent)
        self.app.treeview_operations.renumber_children(target_parent)

        # Push move operation to undo stack
        self.app.undo_stack.append(
            {
                "type": "move",
                "original_positions": self.drag_data["original_positions"],
                "new_positions": new_positions,
            }
        )

    def move_items_up_one_level(self):
        selected_items = self.app.tree.selection()
        original_positions = []

        for item in selected_items:
            parent = self.app.tree.parent(item)
            if parent:
                grandparent = self.app.tree.parent(parent)
                if grandparent:
                    original_parent = parent
                    original_index = self.app.tree.index(item)

                    # Capture the original positions before the move
                    original_positions.append(
                        {
                            "item": item,
                            "original_parent": original_parent,
                            "original_index": original_index,
                        }
                    )

                    # Perform the move
                    self.app.tree.move(
                        item, grandparent, self.app.tree.index(parent) + 1
                    )
                    self.app.treeview_operations.renumber_children(grandparent)

        # After moving, store the operation in the undo stack
        if original_positions:
            self.app.undo_stack.append(
                {"type": "move_up", "original_positions": original_positions}
            )

    def move_items_down_one_level(self):
        selected_items = self.app.tree.selection()
        original_positions = []

        for item in selected_items:
            previous_sibling = self.app.tree.prev(item)
            if previous_sibling:
                original_parent = self.app.tree.parent(item)
                original_index = self.app.tree.index(item)

                # Capture the original positions before the move
                original_positions.append(
                    {
                        "item": item,
                        "original_parent": original_parent,
                        "original_index": original_index,
                    }
                )

                # Perform the move
                self.app.tree.move(item, previous_sibling, "end")
                self.app.treeview_operations.renumber_children(previous_sibling)

        # After moving, store the operation in the undo stack
        if original_positions:
            self.app.undo_stack.append(
                {"type": "move_down", "original_positions": original_positions}
            )
