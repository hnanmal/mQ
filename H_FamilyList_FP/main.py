# src/main.py
import tkinter as tk
from tkinter import ttk
import sys
from src.views.ui import (
    create_other_tab,
    create_family_standard_tab,
)
from src.models.configuration import load_config, save_config

# from src.models.wm_group import WMGroupManager
from src.controllers.logic import initialize_app, lock_toggle_logic
from src.controllers.event_dispatcher import dispatch_event
from src.views.logging_utils import (
    setup_logging_frame,
)  # Import the logging setup function

from src.views.treeview_utils import *
from src.models.tree_model import load_json_data, save_json_data
from src.views.ui import create_family_standard_tab
from src.views.treeview_handlers import handle_copy, handle_paste


def main():
    state, wm_group_manager = initialize_app()

    # Initialize the main Tkinter window
    root = tk.Tk()
    root.title("H Family List")
    root.geometry("1400x900")

    # Create the notebook (tab container)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Set up the logging area and get the logging text widget
    logging_text_widget = setup_logging_frame(root)

    # Create the Family Standard Configuration tab
    create_family_standard_tab(root, notebook, state, logging_text_widget)

    # List of tab names
    other_tab_names = [
        # "패밀리 표준 구성도",  # Family Standard Configuration
        "WM 그룹별 매칭",  # WM Group Matching
        "계산 기준",  # Calculation Criteria
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

    # Create other tabs
    for name in other_tab_names:
        create_other_tab(notebook, name)

    # Debugging: Print statement to confirm main function is running
    logging_text_widget.write("Application Started.")

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
