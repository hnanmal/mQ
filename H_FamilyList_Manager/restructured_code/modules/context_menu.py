import tkinter as tk
from tkinter import Menu

class ContextMenuManager:
    def __init__(self, app):
        self.app = app
        self.menu = None
        self.setup_context_menu()

    def setup_context_menu(self):
        # Create the context menu
        self.menu = Menu(self.app, tearoff=0)
        self.menu.add_command(label="Add Item", command=self.add_item)
        self.menu.add_command(label="Remove Item", command=self.remove_item)
        self.menu.add_separator()
        self.menu.add_command(label="Collapse All", command=self.collapse_all)
        self.menu.add_command(label="Expand All", command=self.expand_all)

    def on_button_click(self, button_name):
        print(f"Button {button_name} clicked!")
        # Implement additional button click logic if needed

    def show_context_menu(self, event):
        # Show the context menu at the cursor location
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def add_item(self):
        self.app.treeview_operations.add_item()
        print("Add Item selected")

    def remove_item(self):
        self.app.treeview_operations.remove_selected_item()
        print("Remove Item selected")

    def collapse_all(self):
        self.app.treeview_operations.collapse_all()
        print("Collapse All selected")

    def expand_all(self):
        self.app.treeview_operations.expand_all()
        print("Expand All selected")

