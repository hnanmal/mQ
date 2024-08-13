# Version: 1.0.0
import tkinter as tk
from tkinter import messagebox
import keyboard


class DragAndDropManager:
    def __init__(self, app):
        self.app = app
        self.drag_data = {"x": 0, "y": 0, "items": []}

        # Track if Alt key is held down
        self.alt_key_down = False
        self.app.bind_all("<Alt_L>", self.alt_key_pressed)
        self.app.bind_all("<KeyRelease-Alt_L>", self.alt_key_released)

    def alt_key_pressed(self, event):
        self.alt_key_down = True
        # self.app.alt_key_down = event.keycode == 64
        print("alt!!")

    def alt_key_released(self, event):
        self.alt_key_down = False
        # self.app.alt_key_down = event.keycode != 64
        print("release alt!!")

    # Bind Alt key for temporary Order Adjustment Mode

    def toggle_order_adjustment_mode(self):
        self.app.order_adjustment_mode.set(not self.app.order_adjustment_mode.get())
        mode_text = "ON" if self.app.order_adjustment_mode.get() else "OFF"
        self.app.order_adjustment_button.config(
            text=f"Order Adjustment Mode: {mode_text}"
        )
        # Only enable drag-and-drop bindings when order adjustment mode is ON
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

    def on_drag_motion(self, event):
        if not self.app.order_adjustment_mode.get() and not self.app.alt_key_down:
            return
        if self.drag_data["items"]:
            for item in self.drag_data["items"]:
                self.app.tree.selection_set(item)
            self.app.tree.focus(self.drag_data["items"][0])

    def on_drag_release(self, event):
        if not self.app.order_adjustment_mode.get() and not self.app.alt_key_down:
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
            self.app.config_manager.move_items(self.drag_data["items"], target_item)

        # Ensure all UI updates are complete before removing selection
        self.app.update_idletasks()

        # Clear the selection after moving
        self.app.tree.selection_remove(self.app.tree.selection())
        self.drag_data = {"x": 0, "y": 0, "items": []}

    def move_items_up_one_level(self):
        selected_items = self.app.tree.selection()
        for item in selected_items:
            parent = self.app.tree.parent(item)
            if parent:
                grandparent = self.app.tree.parent(parent)
                if grandparent:
                    self.app.tree.move(
                        item, grandparent, self.app.tree.index(parent) + 1
                    )
                    self.app.treeview_operations.renumber_children(grandparent)
        # tk.messagebox.showinfo("Level Change", "Selected items moved up one level.")

    def move_items_down_one_level(self):
        selected_items = self.app.tree.selection()
        for item in selected_items:
            previous_sibling = self.app.tree.prev(item)
            if previous_sibling:
                self.app.tree.move(item, previous_sibling, "end")
                self.app.treeview_operations.renumber_children(previous_sibling)
        # tk.messagebox.showinfo("Level Change", "Selected items moved down one level.")
