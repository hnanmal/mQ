# Version: 1.0.6

import tkinter as tk
from tkinter import ttk
from ui import create_single_area_tab, create_three_area_tab
from config_management import ConfigurationManager
from context_menu import ContextMenuManager
from search import SearchManager
from treeview_operations import TreeviewOperations


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tabbed Page App")
        self.geometry("1400x900")  # Window size

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
        self.config_manager = ConfigurationManager(self)
        self.treeview_operations = TreeviewOperations(self)
        self.context_menu_manager = ContextMenuManager(self)
        self.search_manager = SearchManager(self)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
