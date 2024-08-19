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
        self.previous_level_limit = 3  # Default value

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
            2:
        ]  # Top-level items without numbers and periods

        # Create tabs with the specified names
        for i, name in enumerate(tab_names):
            if name == "형식 표준 구성도":
                create_single_area_tab(self, name)
            else:
                create_three_area_tab(self, name)

        # Initialize TreeviewOperations after the tree is created
        self.treeview_operations = TreeviewOperations(self)

        # Track whether the item is in text editing mode
        self.is_text_editing = False

    def undo(self, event=None):
        """Handle the undo operation by delegating to FileUtils."""
        FileUtils.undo_last_action(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    # root = tk.Tk()
    # app = App(root)
    # app.mainloop()
