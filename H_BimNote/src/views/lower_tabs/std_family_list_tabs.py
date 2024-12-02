import tkinter as tk
import tkinter.font

# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.controllers.widget.widgets import (
    EditModeManager,
    handle_add_button_press,
    handle_del_button_press,
)
from src.views.widget.sheet_utils import (
    # add_edit_mode_radio_buttons,
    TeamStd_WMsSheetView,
)
from src.views.widget.treeview_utils import (
    TeamStd_FamlistTreeView,
    TeamStd_GWMTreeView,
    DefaultTreeViewStyleManager,
    TeamStd_WMmatching_TreeView,
    TeamStd_SWMTreeView,
)


def create_stdFamList_tab(state, subtab_notebook):
    edit_mode_manager = EditModeManager()

    working_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(working_tab, text="Standard Family List")

    working_tab_common_area = ttk.Frame(
        working_tab,
        # width=2000,
        height=10,
    )
    working_tab_common_area.pack(expand=True, fill="x")

    working_tab_paned_area = ttk.Frame(
        working_tab,
        # width=600,
        height=3000,
    )
    working_tab_paned_area.pack(expand=True, fill="both")

    working_tab_paned_window = tk.PanedWindow(
        working_tab_paned_area,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    working_tab_paned_window.pack(expand=True, fill="both")

    section1 = ttk.Frame(
        working_tab_paned_area,
        width=1500,
        height=3000,
    )
    section2 = ttk.Frame(
        working_tab_paned_area,
        width=600,
        height=3000,
    )
    # section3 = ttk.Frame(
    #     working_tab_paned_area,
    #     width=600,
    #     height=3000,
    # )

    working_tab_paned_window.add(section1, minsize=400)
    working_tab_paned_window.add(section2, minsize=400)
    # working_tab_paned_window.add(section3, minsize=600)

    working_tab_paned_window.paneconfigure(section1, width=1500, height=3000)
    working_tab_paned_window.paneconfigure(section2, width=600, height=3000)
    # working_tab_paned_window.paneconfigure(section3, height=3000)

    # common 영역 라벨링
    working_tab_font = tk.font.Font(
        family="맑은 고딕",
        size=12,
        # weight="bold",
    )

    # Place tksheet in G-WM tab
    ##############################################################
    ## tab_common_area###########

    # Create an "Edit Mode" / "Locked Mode" button
    edit_mode_button = tk.Button(
        working_tab_common_area,
        text="Locked Mode",
        command=lambda: edit_mode_manager.set_edit_mode(
            "edit" if edit_mode_button.cget("text") == "Locked Mode" else "locked"
        ),
    )
    edit_mode_button.pack(anchor="w", pady=5)

    ##############################################################
    ## section 1###########
    stdFamlist_treeview = TeamStd_FamlistTreeView(state, section1)
    DefaultTreeViewStyleManager.apply_style(stdFamlist_treeview.treeview.tree)

    # Register widgets with EditModeManager
    edit_mode_manager.register_widgets(
        mode_button=edit_mode_button,
        tree_views=[
            stdFamlist_treeview,
        ],
        # tree_ctrl_btn=[
        #     add_button,
        #     del_button,
        # ],
        # sheet=WMs_sheet,
    )

    # Set the initial state to "Locked Mode"
    edit_mode_manager.set_edit_mode("locked")

    return working_tab
