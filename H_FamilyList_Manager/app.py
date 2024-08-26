# Version: 1.0.6

import tkinter as tk
from tkinter import simpledialog, ttk
import json

from utils import FileUtils
from ui import create_single_area_tab, create_three_area_tab
from clipboard import ClipboardManager
from drag_and_drop import DragAndDropManager
from config_management import ConfigurationManager
from context_menu import ContextMenuManager
from search import SearchManager
from treeview_operations import TreeviewOperations
from ui import create_wm_matching_by_group_tab


# from dialogs import ColumnSelectionDialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Existing initialization code...

        # Initialize an undo stack to keep track of changes
        self.undo_stack = []

        # Bind Ctrl-Z to the undo function
        self.bind_all("<Control-z>", self.undo)

        self.title("Tabbed Page App")
        self.geometry("1400x900")  # Window size

        # # Initialize the Treeview early in the __init__ process
        # self.wm_group_treeview = None

        # # Create Treeview ### mk
        # self.tree = ttk.Treeview(
        #     self, show="tree"
        # )  # Use show="tree" to avoid showing placeholders

        # Initialize previous level limit
        self.previous_level_limit = 7  # Default value

        # Initialize original_names attribute
        self.original_names = {}  # Added attribute for storing original names

        # Create a notebook (tabbed pane)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Create treeview
        self.tree = ttk.Treeview(self)  # Initialize treeview directly

        # Initialize managers and operations
        # self.dialog = ColumnSelectionDialog(self)
        self.config_manager = ConfigurationManager(self)
        self.drag_and_drop_manager = DragAndDropManager(self)
        self.clipboard_manager = ClipboardManager(self)
        self.context_menu_manager = ContextMenuManager(self)
        self.search_manager = SearchManager(self)
        self.treeview_operations = TreeviewOperations(self)

        self.ctrl_space_down = False
        self.bind_all("<Control-space>", self.drag_and_drop_manager.ctrl_space_pressed)

        # List of tab names and top-level item names
        tab_names = [
            "형식 표준 구성도",
            "WM 그룹별 매칭",
            "계산 기준",
            "Room",
            "Floors",
            "Roofs",
            "Walls_Ext",
            "Walls_Int",
            "St_Fdn",
            "St_Col",
            "St_Framing",
            "Ceilings",
            "Doors",
            "Windows",
            "Stairs",
            "Railings",
            "Generic",
            "Manual_Input",
        ]
        self.top_level_items = tab_names[
            3:
        ]  # Top-level items without numbers and periods

        # Create tabs with the specified names
        for i, name in enumerate(tab_names):
            if name == "형식 표준 구성도":
                create_single_area_tab(self, name)

            # Initialize the new "WM 그룹별 매칭" tab
            elif name == "WM 그룹별 매칭":
                create_wm_matching_by_group_tab(self)
            else:
                create_three_area_tab(self, name)

        # # Initialize TreeviewOperations after the tree is created
        # self.treeview_operations = TreeviewOperations(self)

        # Load the default configuration on startup
        self.config_manager.load_configuration(file_path="defaultTypeTree.json")

        # Track whether the item is in text editing mode
        self.is_text_editing = False

        # Load WM Group Match data from JSON
        self.wm_group_match_data = self.load_wm_group_match_data()

    def undo(self, event=None):
        """Handle the undo operation by delegating to FileUtils."""
        FileUtils.undo_last_action(self)

    def update_wm_group_matching_treeview(self, level_6_items):
        # Clear the current content of the Treeview
        self.wm_group_treeview.delete(*self.wm_group_treeview.get_children())

        # Insert the unique names into the Treeview
        for name in level_6_items:
            self.wm_group_treeview.insert("", tk.END, values=(name,))

    def update_center_title_label(self, event):
        # Reload the WM Group Match data from the JSON file
        self.wm_group_match_data = self.load_wm_group_match_data()

        # Get the selected item
        selected_item = self.wm_group_treeview.selection()

        if selected_item:
            # Get the value of the selected item (the name)
            item_name = self.wm_group_treeview.item(selected_item[0], "values")[0]

            # Update the center title label with the selected item's name
            self.center_title_label.config(text=item_name)

            # Clear the current content in the center area
            self.drop_area.delete(0, tk.END)

            # Check if there is matching data in wm_group_match.json
            if item_name in self.wm_group_match_data:
                # Populate the center area with the matched data
                for entry in self.wm_group_match_data[item_name]:
                    self.drop_area.insert(tk.END, entry)
            else:
                # If no match is found, leave the area empty
                self.drop_area.insert(tk.END, "No matching data found.")

            # Update the lock button state and center area background color
            is_locked = self.lock_status.get(item_name, False)
            self.lock_button.config(text="Unlock" if is_locked else "Lock")
            self.drop_area.config(bg="gray" if is_locked else "white")

        else:
            # Clear the label if no item is selected
            self.center_title_label.config(text="")

    def load_wm_group_match_data(self):
        try:
            with open("wm_group_match.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # Update lock status based on the JSON data
                self.lock_status = data.get("lock_status", {})
                # Apply the lock status to the treeview items
                for item in self.wm_group_treeview.get_children():
                    item_name = self.wm_group_treeview.item(item, "values")[0]
                    is_locked = self.lock_status.get(item_name, False)
                    if is_locked:
                        self.wm_group_treeview.item(item, tags=("locked",))
                    else:
                        self.wm_group_treeview.item(item, tags=("unlocked",))
                return data
        except FileNotFoundError:
            return {}

    def save_lock_status(app):
        try:
            with open("wm_group_match.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data["lock_status"] = app.lock_status

        with open("wm_group_match.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app = App()
    app.mainloop()
