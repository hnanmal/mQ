# src/views/notebook_tabs.py

import tkinter as tk
from tkinter import ttk
from src.controllers.event_management import handle_tab_click
from src.views.wm_group_matching import create_wm_group_matching_tab
from src.views.tree_management import create_family_standard_tab, create_sub_tab
from src.tabs.project_info_tab.project_info_tab import create_project_info_tab
from src.tabs.input_common_tab.input_common_tab import create_input_common_tab
from src.tabs.calc_criteria_tab.calc_criteria_tab import create_calc_criteria_tab


def create_notebook_with_tabs(root, state):
    main_notebook = ttk.Notebook(root, style="Upper.TNotebook")

    return main_notebook


def create_team_standard_tab(root, notebook, state, wm_group_manager):
    """Create the Team Standard tab with its sub-tabs."""
    team_standard_tab = ttk.Frame(notebook)
    notebook.add(team_standard_tab, text="Team Standard")

    team_notebook = ttk.Notebook(
        team_standard_tab, style="Lower.TNotebook"
    )  # Lower-level notebook
    team_notebook.pack(fill="both", expand=True)

    # Add sub-tabs to the "Team Standard" tab
    create_family_standard_tab(root, team_notebook, state)
    create_wm_group_matching_tab(team_notebook, state, wm_group_manager)

    # Bind the tab click event
    team_notebook.bind(
        "<Button-1>", lambda event: handle_tab_click(event, team_notebook, state)
    )


def create_project_standard_tab(notebook, state):
    """Create the Project Standard tab with its sub-tabs."""
    project_standard_tab = ttk.Frame(notebook)
    notebook.add(project_standard_tab, text="Project Standard")  # Use larger tab style

    project_notebook = ttk.Notebook(
        project_standard_tab, style="Lower.TNotebook"
    )  # Lower-level notebook
    project_notebook.pack(fill="both", expand=True)

    # Create the "프로젝트 정보 입력" tab
    create_project_info_tab(project_notebook, state)
    create_input_common_tab(project_notebook, state)
    create_calc_criteria_tab(project_notebook, state)

    # other_tab_names = [
    #     # "프로젝트 정보 입력",
    #     # "공통입력",
    #     # "산출기준",
    #     "Room",
    #     "Floors",
    #     "Roofs",
    #     "Walls_Ext",
    #     "Walls_Int",
    #     "St_Fdn",
    #     "St_Col",
    #     "St_Framing",
    #     "Ceilings",
    #     "Doors",
    #     "Windows",
    #     "Stairs",
    #     "Railings",
    #     "Generic",
    #     "Manual_Input",
    # ]

    # for name in other_tab_names:
    #     create_sub_tab(project_notebook, name)

    # Bind the tab click event
    project_notebook.bind(
        "<Button-1>", lambda event: handle_tab_click(event, project_notebook, state)
    )


def create_family_linkage_tab(notebook, state):
    """Create the Project Standard tab with its sub-tabs."""
    family_linkage_tab = ttk.Frame(notebook)
    notebook.add(family_linkage_tab, text="패밀리 타입 관리")  # Use larger tab style

    project_notebook = ttk.Notebook(
        family_linkage_tab, style="Lower.TNotebook"
    )  # Lower-level notebook
    project_notebook.pack(fill="both", expand=True)

    # Create the "프로젝트 정보 입력" tab
    other_tab_names = [
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

    for name in other_tab_names:
        create_sub_tab(project_notebook, name)

    # Bind the tab click event
    project_notebook.bind(
        "<Button-1>", lambda event: handle_tab_click(event, project_notebook, state)
    )
