import tkinter as tk
from tkinter import ttk

from src.controllers.state_controllers import handle_tab_click
from src.views.sub_tabs import create_family_standard_tab


def create_notebook_with_tabs(root, state):
    main_notebook = ttk.Notebook(root, style="Upper.TNotebook")

    return main_notebook


def create_team_standard_tab(root, notebook, state):
    """Create the Team Standard tab with its sub-tabs."""
    team_standard_tab = ttk.Frame(notebook)
    notebook.add(team_standard_tab, text="Team Standard")

    team_notebook = ttk.Notebook(
        team_standard_tab, style="Lower.TNotebook"
    )  # Lower-level notebook
    team_notebook.pack(fill="both", expand=True)

    # Add sub-tabs to the "Team Standard" tab
    create_family_standard_tab(root, team_notebook, state)
    # create_wm_group_matching_tab(team_notebook, state, wm_group_manager)

    # Bind the tab click event
    team_notebook.bind(
        "<Button-1>", lambda event: handle_tab_click(event, team_notebook, state)
    )
