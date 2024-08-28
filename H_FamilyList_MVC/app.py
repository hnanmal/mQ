import tkinter as tk
from tkinter import simpledialog, ttk
from utils import FileUtils

# Model import
from models.wm_group import (
    load_wm_group_match_data,
    # save_lock_status_to_json,
    # save_current_matching_to_json,
    # filter_excel_data,
    # save_configuration,
    load_configuration,
)
from models.configuration import ConfigurationManager


# View import
from views.ui import UIManager

# Controller import
from controllers.main_controller import (
    on_item_double_click,
    on_item_single_click,
    update_center_title_label,
)
from controllers.ui_controller import (
    add_item_to_center,
    remove_item_from_center,
    toggle_lock,
)

# Other necessary imports
from controllers.clipboard import ClipboardManager
from controllers.drag_and_drop import DragAndDropManager

# from config_management import ConfigurationManager
from context_menu import ContextMenuManager
from search import SearchManager
from controllers.treeview_operations import TreeviewOperations


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # def test_right_click(event):
        #     print("Right-click detected in test")

        # self.bind("<Button-3>", test_right_click)

        # Initialize an undo stack to keep track of changes
        self.undo_stack = []

        # Bind Ctrl-Z to the undo function
        self.bind_all("<Control-z>", self.undo)

        self.title("MVC Refactoring")
        self.geometry("1400x900")  # Window size

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
        self.ui_manager = UIManager(self)
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
            "패밀리 표준 구성도",
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
        for name in tab_names:
            if name == "패밀리 표준 구성도":
                self.ui_manager.create_single_area_tab(self, name)
                # create_single_area_tab(self, name)
            elif name == "WM 그룹별 매칭":
                self.ui_manager.create_wm_matching_by_group_tab(self)
                # create_wm_matching_by_group_tab(self)
            else:
                self.ui_manager.create_three_area_tab(self, name)

        # Load the default configuration on startup
        load_configuration(self, file_path="defaultTypeTree.json")

        # Track whether the item is in text editing mode
        self.is_text_editing = False

        # Load WM Group Match data from JSON
        self.wm_group_match_data = load_wm_group_match_data(self)

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
        self.wm_group_match_data = load_wm_group_match_data(self)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
