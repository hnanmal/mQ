import tkinter as tk
import tkinter.font
from PIL import Image, ImageTk
from html.parser import HTMLParser

# from tkhtmlview import HTMLLabel
# from cefpython3 import cefpython as cef

# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.controllers.widget.widgets import EditModeManager
from src.views.widget.treeview_utils import BuildingList_TreeView
from src.views.widget.dnd_utils import FilePathRegister
from src.views.widget.html_viewer import BrowserWidget
from src.views.widget.pjt_main_widget import ProjectInfoWidget, ProjectStdDashboard


def create_pjtStd_Main_tab(state, subtab_notebook, exe_mode=None):

    edit_mode_manager = EditModeManager()

    working_tab = ttk.Frame(subtab_notebook)

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

    if not exe_mode:
        subtab_notebook.add(working_tab, text="Project Standard Main")

    section1 = ttk.Frame(
        working_tab_paned_area,
        width=1000,
        height=3000,
    )
    section2 = ttk.Frame(
        working_tab_paned_area,
        width=1000,
        height=3000,
    )
    section3 = ttk.Frame(
        working_tab_paned_area,
        width=1000,
        height=3000,
    )

    working_tab_paned_window.add(section1, minsize=400)
    working_tab_paned_window.paneconfigure(section1, height=3000)

    working_tab_paned_window.add(section2, minsize=400)
    working_tab_paned_window.paneconfigure(section2, height=3000)

    working_tab_paned_window.add(section3, minsize=400)
    working_tab_paned_window.paneconfigure(section3, height=3000)

    # common 영역 라벨링
    working_tab_font = tk.font.Font(
        family="맑은 고딕",
        size=12,
        # weight="bold",
    )

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

    ProjectInfoWidget(state, section1)

    ##############################################################
    ## section 2###########
    pjt_stdDashboard_area = ttk.Frame(
        section2,
        width=600,
    )
    pjt_stdDashboard_area.pack()

    ProjectStdDashboard(state, pjt_stdDashboard_area)
    ##############################################################
    ## section 3###########

    return working_tab_paned_window
