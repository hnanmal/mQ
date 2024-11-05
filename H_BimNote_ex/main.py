import tkinter as tk
from tkinter import ttk

from src.controllers.app_setup import initialize_app
from src.views.styles import configure_tab_styles
from src.views.tabs import create_notebook_with_tabs, create_team_standard_tab
from src.views.logging_utils import setup_logging_frame


def main():
    # Initialize the main Tkinter window
    root = tk.Tk()
    root.title("H_bimNote")
    root.iconbitmap("resources/favicon_io/favicon.ico")

    root.geometry(
        "{}x{}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())
    )
    root.state("zoomed")  # Maximizes the window while keeping window controls visible

    configure_tab_styles()  # Configure the tab style

    logging_text_widget = setup_logging_frame(root)

    # Log the start of loading
    logging_text_widget.write("Configuring system...\n")

    # initiate app_state
    app_state = initialize_app(logging_text_widget, root=root)

    main_notebook = create_notebook_with_tabs(root, app_state)
    main_notebook.pack(fill="both", expand=True)

    # Create upper-level tabs: Team Standard and Project Standard
    create_team_standard_tab(root, main_notebook, app_state)
    # create_project_standard_tab(main_notebook, app_state)
    # create_familyType_manage_tab(main_notebook, app_state)

    # # Debugging: Print statement to confirm main function is running
    logging_text_widget.write("안녕하세요. 어플리케이션이 시작 되었습니다.\n")
    # main_notebook.select(1)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
