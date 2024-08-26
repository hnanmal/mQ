# app.py

import tkinter as tk
from tkinter import ttk
from modules.ui import UIManager
from modules.data_manager import load_wm_group_match_data
from modules.operations import WM_group_tab_CenterAreaOperations
from modules.treeview_operations import TreeviewOperations
from modules.drag_and_drop import DragAndDropManager
from modules.clipboard import ClipboardManager
from modules.context_menu import ContextMenuManager
from modules.search import SearchManager
from modules.config_management import ConfigurationManager
from modules.tabs.wm_group_tab import WM_group_tab_Manager


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize undo stack to keep track of changes
        self.undo_stack = []

        # Bind the undo operation to Ctrl+Z
        self.bind_all("<Control-z>", lambda event: self.treeview_operations.undo())

        self.title("Tabbed Page App")
        self.geometry("1400x900")  # Set the window size

        # Set the initial previous_level_limit to some default value, e.g., 7
        self.previous_level_limit = 7

        # Initialize operations
        self.original_names = {}  # Initialize original_names here

        # Initialize the notebook (tabbed pane)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Initialize the treeview early in the process
        self.tree = ttk.Treeview(self)  # Create the treeview widget

        # Initialize managers and operations
        self.config_manager = ConfigurationManager(self)
        self.drag_and_drop_manager = DragAndDropManager(self)
        self.clipboard_manager = ClipboardManager(self)
        self.context_menu_manager = ContextMenuManager(self)
        self.search_manager = SearchManager(self)
        self.treeview_operations = TreeviewOperations(self)
        self.center_operations = WM_group_tab_CenterAreaOperations(self)  # 신설고려

        self.WM_group_tab_Manager = WM_group_tab_Manager

        self.ctrl_space_down = False
        self.bind_all("<Control-space>", self.drag_and_drop_manager.ctrl_space_pressed)

        # Initialize lock status
        self.lock_status = {}

        # Setup the UI using UIManager
        self.ui_manager = UIManager(self)
        self.ui_manager.setup_ui()

        # Load the default configuration on startup
        self.config_manager.load_default_configuration("defaultTypeTree.json")

        # Load the WM Group Match data after the UI is set up
        self.wm_group_match_data = load_wm_group_match_data(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
