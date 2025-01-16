from src.core.fp_utils import *
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
    Project_WM_perRVT_SheetView,
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
from src.views.widget.assign_widget import (
    ModelType_entry,
    TypeAssign_treeview,
    WMapply_button,
)
from src.views.widget.collapsing_frame import CollapsingFrame


def create_pjt_familylist_tab(state, subtab_notebook, exe_mode=None):
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
        subtab_notebook.add(working_tab, text="Project Family Assign")

    section1 = ttk.Frame(
        working_tab_paned_area,
        width=1000,
        height=3000,
    )
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
    cf = CollapsingFrame(state, section3)
    cf.pack(fill=BOTH)

    main_area = ttk.Frame(
        cf,
        # padding=10,
    )

    suggestWM_area = ttk.Frame(
        main_area,
        # padding=10,
    )
    suggestWM_area.pack(anchor="nw")

    GWMarea = ttk.Frame(
        suggestWM_area,
        relief="ridge",
        borderwidth=3,
        # bootstyle="outline",
    )
    GWMarea.pack(side="left", anchor="nw")

    SWMarea = ttk.Frame(
        suggestWM_area,
        relief="ridge",
        borderwidth=3,
        # bootstyle="outline",
    )
    SWMarea.pack(side="left", anchor="nw")

    projectApply_GWM_Selcet_SheetView = ProjectApply_GWMSWM_Selcet_SheetView(
        state,
        GWMarea,
        pjt_famlist,
        typeAssign_treeview,
    )
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(projectApply_GWM_Selcet_SheetView)
    #############################################################################

    projectApply_SWM_Selcet_SheetView = ProjectApply_GWMSWM_Selcet_SheetView(
        state,
        SWMarea,
        pjt_famlist,
        typeAssign_treeview,
        wm_mode="[ SWM ]",
    )
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(projectApply_SWM_Selcet_SheetView)
    #############################################################################

    wm_apply_button = WMapply_button(
        state,
        main_area,
        ref_widgets=[
            pjt_famlist,
            projectApply_GWM_Selcet_SheetView,
            projectApply_SWM_Selcet_SheetView,
            typeAssign_treeview,
        ],
        tgt_widget=None,
    )

    cf.add(
        child=main_area,
        title="Suggested Standard WM items",
        bootstyle="info",
        suggest_area=True,
    )

    # option group 2
    customWM_area = ttk.Frame(
        cf,
        # padding=10,
    )
    state.customWM_area = customWM_area

    def toggle_height(state):
        if state.rvt_wm_isShort == True:
            state.project_WM_perRVT_SheetView.renew_sheet_height()
            state.rvt_wm_isShort = False
        else:
            state.project_WM_perRVT_SheetView.rollback_sheet_height()
            state.rvt_wm_isShort = True

    renew_button = tk.Button(
        customWM_area,
        text="시트 높이조정",
        font=("Arial Narrow", 8, "normal"),
        command=lambda: toggle_height(state),
    )
    renew_button.config(
        width=12,
        height=1,
    )
    renew_button.pack(side="top", anchor="ne")

    project_WM_perRVT_SheetView = Project_WM_perRVT_SheetView(
        state,
        customWM_area,
        typeAssign_treeview,
        height=375,
        # height=100,
    )
    ######### notify_targets 등록 ###############################################
    state.notify_targets.append(project_WM_perRVT_SheetView)
    #############################################################################
    state.project_WM_perRVT_SheetView = project_WM_perRVT_SheetView

    cf.add(
        child=customWM_area,
        # title="Final WM Registration per Rvt Type",
        # collapsed=True,
        collapsed=False,
        textvariable=state.selected_rvtTypes_forLabel,
        bootstyle="primary",
    )

    return working_tab
