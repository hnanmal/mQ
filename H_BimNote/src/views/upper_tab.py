import tkinter as tk
from tkinter import ttk

from src.views.lower_tabs.group_WM_tabs import create_stdGWM_tab, create_stdSWM_tab
from src.views.lower_tabs.common_input_tab import create_common_input_tab
from src.views.lower_tabs.std_family_list_tabs import create_stdFamList_tab
from src.views.lower_tabs.pjt_group_WM_tabs import (
    create_pjtStdGWM_tab,
    create_pjtStdSWM_tab,
)
from src.views.lower_tabs.pjt_std_main_tab import create_pjtStd_Main_tab
from src.views.lower_tabs.pjt_apply_main_tab import create_pjtApply_Main_tab


def create_tab_with_subtabs(state, notebook, tab_name, subtab_names):
    # Create the main tab
    main_frame = ttk.Frame(notebook)
    notebook.add(main_frame, text=tab_name)

    # Create the notebook for subtabs
    subtab_notebook = ttk.Notebook(
        main_frame,
        # style="Subtab.TNotebook",
        bootstyle=state.tab_bootStyle,
    )
    # subtab_notebook = ttk.Notebook(main_frame, style="lefttab.TNotebook")
    subtab_notebook.pack(expand=True, fill="both")

    return subtab_notebook


def create_team_standard_tab(state, notebook):
    subtab_names = ["Lower Tab 1", "Lower Tab 2"]

    subtab_notebook = create_tab_with_subtabs(
        state, notebook, "Team Standard", subtab_names
    )

    g_wm_tab = create_stdGWM_tab(state, subtab_notebook)
    s_wm_tab = create_stdSWM_tab(state, subtab_notebook)
    common_input_tab = create_common_input_tab(state, subtab_notebook)
    std_Famlist_tab = create_stdFamList_tab(state, subtab_notebook)


def create_project_standard_tab(state, notebook):
    subtab_names = ["Lower Tab 1", "Lower Tab 2"]

    subtab_notebook = create_tab_with_subtabs(
        state, notebook, "Project Standard", subtab_names
    )
    main_tab = create_pjtStd_Main_tab(state, subtab_notebook)
    g_wm_tab = create_pjtStdGWM_tab(state, subtab_notebook)
    s_wm_tab = create_pjtStdSWM_tab(state, subtab_notebook)
    common_input_tab = create_common_input_tab(state, subtab_notebook)
    # std_Famlist_tab = create_stdFamList_tab(state, subtab_notebook)


def create_project_apply_tab(state, notebook):
    subtab_names = ["Lower Tab 1", "Lower Tab 2"]

    subtab_notebook = create_tab_with_subtabs(
        state, notebook, "Project Apply", subtab_names
    )

    # Add each subtab
    main_tab = create_pjtApply_Main_tab(state, subtab_notebook)
    for subtab_name in subtab_names:
        subtab_frame = ttk.Frame(subtab_notebook)
        subtab_notebook.add(subtab_frame, text=subtab_name)
