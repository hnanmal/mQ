# Version: 1.0.0

from tkinter import messagebox


class DragAndDropManager:
    def __init__(self, app):
        self.app = app
        self.drag_data = {"x": 0, "y": 0, "items": []}
        self.alt_key_down = False

    def on_drag_start(self, event):
        if not self.app.order_adjustment_mode.get() and not self.alt_key_down:
            return
        items = self.app.tree.selection()
        if items:
            self.drag_data["items"] = items
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        if not self.app.order_adjustment_mode.get() and not self.alt_key_down:
            return
        if self.drag_data["items"]:
            for item in self.drag_data["items"]:
                self.app.tree.selection_set(item)
            self.app.tree.focus(self.drag_data["items"][0])

    def on_drag_release(self, event):
        if not self.app.order_adjustment_mode.get() and not self.alt_key_down:
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
