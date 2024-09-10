# src/main.py
import tkinter as tk
from tkinter import ttk

# import sys
from src.views.ui import (
    create_notebook_with_tabs,
    create_project_standard_tab,
    create_team_standard_tab,
)

from src.controllers.logic import initialize_app

# from src.controllers.event_dispatcher import dispatch_event
from src.views.logging_utils import (
    setup_logging_frame,
)  # Import the logging setup function

from src.views.treeview_utils import *
from src.views.styles import configure_tab_styles


def main():

    # Initialize the main Tkinter window
    root = tk.Tk()
    root.title("H Family List")
    root.geometry("1400x900")

    # Open the window in full screen
    root.state("zoomed")  # Maximizes the window while keeping window controls visible

    configure_tab_styles()  # Configure the tab style

    # Set up the logging area and get the logging text widget
    logging_text_widget = setup_logging_frame(root)

    # Log the start of loading
    logging_text_widget.write("Configuring system...\n")

    # state
    app_state, wm_group_manager = initialize_app(logging_text_widget)

    # Create the notebook (tab container)
    main_notebook = create_notebook_with_tabs(root, app_state)
    main_notebook.pack(fill="both", expand=True)

    # Create upper-level tabs: Team Standard and Project Standard
    create_team_standard_tab(root, main_notebook, app_state, wm_group_manager)
    create_project_standard_tab(main_notebook, app_state)

    # # Debugging: Print statement to confirm main function is running
    # logging_text_widget.write("안녕하세요. 어플리케이션이 시작 되었습니다.\n")

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
