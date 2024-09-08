# # tests/test_core.py

# import unittest
# from src.core.state_management import AppState

# class TestAppState(unittest.TestCase):
#     def test_set_current_tab(self):
#         state = AppState()
#         state.set_current_tab("test_tab")
#         self.assertEqual(state.current_tab, "test_tab")

#     # Add more tests as needed

# if __name__ == "__main__":
#     unittest.main()

import tkinter as tk
from tkinter import ttk

class RibbonMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ribbon Menu Example")
        
        # Create the notebook for the ribbon tabs
        self.ribbon = ttk.Notebook(root)
        self.ribbon.pack(side=tk.TOP, fill=tk.X)

        # Create the tabs for the ribbon menu
        self.create_home_tab()
        self.create_insert_tab()
        self.create_view_tab()

    def create_home_tab(self):
        """Create the Home tab with buttons organized into groups."""
        home_tab = ttk.Frame(self.ribbon)
        self.ribbon.add(home_tab, text="Home")

        # Create a frame for a group of buttons
        clipboard_group = ttk.LabelFrame(home_tab, text="Clipboard", padding=(10, 10))
        clipboard_group.pack(side=tk.LEFT, padx=10, pady=5)

        # Add buttons to the clipboard group
        paste_button = ttk.Button(clipboard_group, text="Paste")
        cut_button = ttk.Button(clipboard_group, text="Cut")
        copy_button = ttk.Button(clipboard_group, text="Copy")

        # Pack buttons inside the group
        paste_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        cut_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        copy_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Create another group of buttons
        font_group = ttk.LabelFrame(home_tab, text="Font", padding=(10, 10))
        font_group.pack(side=tk.LEFT, padx=10, pady=5)

        # Add buttons for font actions
        bold_button = ttk.Button(font_group, text="Bold")
        italic_button = ttk.Button(font_group, text="Italic")
        underline_button = ttk.Button(font_group, text="Underline")

        # Pack font buttons inside the font group
        bold_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        italic_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        underline_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    def create_insert_tab(self):
        """Create the Insert tab."""
        insert_tab = ttk.Frame(self.ribbon)
        self.ribbon.add(insert_tab, text="Insert")

        # Example group for inserting objects
        objects_group = ttk.LabelFrame(insert_tab, text="Objects", padding=(10, 10))
        objects_group.pack(side=tk.LEFT, padx=10, pady=5)

        # Add buttons for inserting objects
        picture_button = ttk.Button(objects_group, text="Picture")
        chart_button = ttk.Button(objects_group, text="Chart")

        # Pack buttons inside the objects group
        picture_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        chart_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    def create_view_tab(self):
        """Create the View tab."""
        view_tab = ttk.Frame(self.ribbon)
        self.ribbon.add(view_tab, text="View")

        # Example group for view controls
        view_group = ttk.LabelFrame(view_tab, text="View Controls", padding=(10, 10))
        view_group.pack(side=tk.LEFT, padx=10, pady=5)

        # Add buttons for zoom and view actions
        zoom_in_button = ttk.Button(view_group, text="Zoom In")
        zoom_out_button = ttk.Button(view_group, text="Zoom Out")

        # Pack buttons inside the view group
        zoom_in_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        zoom_out_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = RibbonMenuApp(root)
    root.geometry("600x400")
    root.mainloop()
