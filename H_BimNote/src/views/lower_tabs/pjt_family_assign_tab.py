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
    ProjectApply_GWMSWM_Selcet_SheetView,
    ProjectStd_WM_Selcet_SheetView_SWM,
    TeamStd_WMsSheetView,
    ProjectStd_WM_Selcet_SheetView_GWM,
)
from src.views.widget.treeview_utils import (
    TeamStd_GWMTreeView,
    DefaultTreeViewStyleManager,
    TeamStd_WMmatching_TreeView,
    TeamStd_SWMTreeView,
    PjtStd_GWMTreeView,
    TeamStd_calcDict_TreeView,
)
from src.views.widget.pjt_familylist_widget import StdFamilyListWidget
from src.views.widget.widget import Builing_select_combobox, Current_building_label
from src.views.widget.assign_widget import ModelType_entry, TypeAssign_treeview
from src.views.widget.collapsing_frame import CollapsingFrame


def create_pjt_familylist_tab(state, subtab_notebook):
    edit_mode_manager = EditModeManager()

    working_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(working_tab, text="Project Family Assign")

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
        width=1000,
        height=3000,
    )
    # state.GWMsection = section1
    section2 = ttk.Frame(
        working_tab_paned_area,
        width=400,
        height=3000,
    )

    section3 = ttk.Frame(
        working_tab_paned_area,
        width=2000,
        height=3000,
    )

    working_tab_paned_window.add(section1)
    working_tab_paned_window.add(section2)
    working_tab_paned_window.add(section3)

    working_tab_paned_window.paneconfigure(
        section1,
        minsize=100,
        # maxsize=1000,
        height=3000,
    )
    working_tab_paned_window.paneconfigure(
        section2,
        minsize=400,
        width=400,
        height=3000,
    )
    working_tab_paned_window.paneconfigure(
        section3,
        minsize=1100,
        height=3000,
    )

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
    edit_mode_button.pack(side="left", anchor="nw", pady=5)

    builing_select_combobox = Builing_select_combobox(state, working_tab_common_area)
    state.builing_select_combobox = builing_select_combobox

    ##############################################################
    ## section 1###########
    pjt_famlist = StdFamilyListWidget(state, section1)

    ##############################################################
    ## section 2###########
    curBuilding_widget = Current_building_label(state, section2)

    modelType_entry = ModelType_entry(state, section2, relate_widget=pjt_famlist)

    typeAssign_treeview = TypeAssign_treeview(
        state, section2, relate_widget=modelType_entry
    )
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(typeAssign_treeview)
    #############################################################################
    # state.typeAssign_treeview = typeAssign_treeview

    # calc_dict Area
    calc_dict_area = ttk.Frame(section2)
    calc_dict_area.pack(fill="x", side="bottom", anchor="s", padx=20)
    pjtAssign_calcDict_TreeView = TeamStd_calcDict_TreeView(
        state,
        calc_dict_area,
        relate_widget=pjt_famlist,
        view_level=3,
    )
    pjtAssign_calcDict_TreeView.treeview.tree.config(height=4)
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(pjtAssign_calcDict_TreeView)
    #############################################################################
    # state.pjtAssign_calcDict_TreeView = pjtAssign_calcDict_TreeView

    ##############################################################
    ## section 3###########
    cf = CollapsingFrame(section3)
    cf.pack(fill=BOTH)

    suggestWM_area = ttk.Frame(
        cf,
        # padding=10,
    )

    projectApply_GWM_Selcet_SheetView = ProjectApply_GWMSWM_Selcet_SheetView(
        state,
        suggestWM_area,
        pjt_famlist,
        typeAssign_treeview,
    )
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(projectApply_GWM_Selcet_SheetView)
    #############################################################################

    projectApply_SWM_Selcet_SheetView = ProjectApply_GWMSWM_Selcet_SheetView(
        state,
        suggestWM_area,
        pjt_famlist,
        typeAssign_treeview,
        wm_mode="[ SWM ]",
    )
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(projectApply_SWM_Selcet_SheetView)
    #############################################################################

    # for x in range(35):
    #     ttk.Checkbutton(suggestWM_area, text=f"Option {x + 1}").pack(fill=X)
    # StdFamilyListWidget(state, suggestWM_area)
    cf.add(
        child=suggestWM_area, title="Suggested Standard WM items", bootstyle="primary"
    )

    # option group 2
    customWM_area = ttk.Frame(
        cf,
        # padding=10,
    )
    for x in range(35):
        ttk.Checkbutton(customWM_area, text=f"Option {x + 1}").pack(fill=X)
    cf.add(
        child=customWM_area,
        title="User addition WM items",
        bootstyle="info",
        collapsed=True,
    )
