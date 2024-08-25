import tkinter as tk
from tkinter import ttk

class DragAndDropManager:
    def __init__(self, app):
        self.app = app

    def toggle_order_adjustment_mode(self):
        self.order_adjustment_mode = not self.order_adjustment_mode
        mode_text = "ON" if self.order_adjustment_mode else "OFF"
        self.app.order_adjustment_button.config(text=f"Order Adjustment Mode: {mode_text}")

        # Implement any additional logic needed to toggle order adjustment mode
        if self.order_adjustment_mode:
            # Code to enable order adjustment mode
            pass
        else:
            # Code to disable order adjustment mode
            pass

    def enable_drag_and_drop(self):
        def on_drag_start(event, treeview):
            if treeview == self.app.wm_group_treeview:
                return
            self.selected_items = treeview.selection()
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
            self.app.bind("<B1-Motion>", lambda e: initiate_drag(e, treeview))
            self.app.bind("<ButtonRelease-1>", on_drop)

        def initiate_drag(event, treeview):
            dx = abs(event.x_root - self.drag_start_x)
            dy = abs(event.y_root - self.drag_start_y)
            selected_items = self.selected_items
            if dx > 5 or dy > 5:
                if hasattr(self, "dragged_items"):
                    del self.dragged_items
                if selected_items:
                    self.dragged_items = [(treeview, item) for item in selected_items]
                    item_texts = [treeview.item(item, "values")[0] for item in selected_items]
                    if hasattr(self, "drag_label"):
                        self.drag_label.destroy()
                    self.drag_label = ttk.Label(self.app, text=",\n ".join(item_texts))
                    self.drag_label.place(x=event.x_root, y=event.y_root)
                    self.app.bind("<B1-Motion>", on_drag_motion)

        def on_drag_motion(event):
            if hasattr(self, "drag_label"):
                self.drag_label.place(x=event.x_root, y=event.y_root)

        def on_drop(event):
            if not hasattr(self, "dragged_items"):
                return
            widget_under_mouse = self.app.winfo_containing(event.x_root, event.y_root)
            if widget_under_mouse == self.app.drop_area:
                for treeview, item in self.dragged_items:
                    item_text = treeview.item(item, "values")[0]
                    self.app.drop_area.insert(tk.END, item_text)
            if hasattr(self, "drag_label"):
                self.drag_label.destroy()
                del self.drag_label
            if hasattr(self, "dragged_items"):
                del self.dragged_items
            self.app.unbind("<B1-Motion>")
            self.app.unbind("<ButtonRelease-1>")

        self.app.excel_treeview.bind("<ButtonPress-1>", lambda e: on_drag_start(e, self.app.excel_treeview))

