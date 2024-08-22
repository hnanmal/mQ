# Version: 1.0.6

import tkinter as tk
from tkinter import simpledialog, ttk

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

        # Create Treeview ### mk
        self.tree = ttk.Treeview(
            self, show="tree"
        )  # Use show="tree" to avoid showing placeholders

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

        # Initialize TreeviewOperations after the tree is created
        self.treeview_operations = TreeviewOperations(self)

        # Load the default configuration on startup
        self.config_manager.load_configuration(file_path="defaultTypeTree.json")

        # Track whether the item is in text editing mode
        self.is_text_editing = False

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
        # Get the selected item
        selected_item = self.wm_group_treeview.selection()

        if selected_item:
            # Get the value of the selected item (the name)
            item_name = self.wm_group_treeview.item(selected_item[0], "values")[0]

            # Update the center title label with the selected item's name
            self.center_title_label.config(text=item_name)
        else:
            # Clear the label if no item is selected
            self.center_title_label.config(text="")


if __name__ == "__main__":
    app = App()
    app.mainloop()
