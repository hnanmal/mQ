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
    ProjectStd_WM_Selcet_SheetView,
)
from src.views.widget.treeview_utils import (
    TeamStd_GWMTreeView,
    DefaultTreeViewStyleManager,
    TeamStd_WMmatching_TreeView,
    TeamStd_SWMTreeView,
)


def create_pjtStdGWM_tab(state, subtab_notebook):
    edit_mode_manager = EditModeManager()

    working_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(working_tab, text="Standard Work Master : Group (Std G-WM)")

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
        width=600,
        height=3000,
    )
    section3 = ttk.Frame(
        working_tab_paned_area,
        width=600,
        height=3000,
    )

    working_tab_paned_window.add(section1, minsize=400)
    working_tab_paned_window.add(section2, minsize=400)
    working_tab_paned_window.add(section3, minsize=600)

    working_tab_paned_window.paneconfigure(section1, height=3000)
    working_tab_paned_window.paneconfigure(section2, width=600, height=3000)
    working_tab_paned_window.paneconfigure(section3, height=3000)

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
    pjtStdGWM_treeview = TeamStd_GWMTreeView(state, section1)
    DefaultTreeViewStyleManager.apply_style(pjtStdGWM_treeview.treeview.tree)
    state.pjtStdGWM_treeview = pjtStdGWM_treeview

    ##############################################################
    ## section 2###########
    selected_item_label_area = ttk.Frame(
        section2,
        width=600,
    )
    selected_item_label_area.pack(side=tk.TOP, anchor="w")

    selected_item_label = ttk.Label(
        selected_item_label_area,
        text="Selected Item: ",
        font=working_tab_font,
    )
    selected_item = ttk.Label(
        selected_item_label_area,
        # textvariable=state.selected_stdGWM_item,
        textvariable=pjtStdGWM_treeview.selected_item,
        font=working_tab_font,
        foreground="blue",
    )
    selected_item_label.pack(side="left", padx=5, pady=5, anchor="w")
    selected_item.pack(side="left", padx=5, pady=5, anchor="w")

    std_matching_widget_area = ttk.Frame(
        section2,
        width=600,
    )
    std_matching_widget_area.pack(side="top", anchor="w")

    pjtStd_matching_treeview = ProjectStd_WM_Selcet_SheetView(
        state, std_matching_widget_area
    )

    # pjtStd_matching_treeview = TeamStd_WMmatching_TreeView(
    #     state, std_matching_widget_area, pjtStdGWM_treeview, data_kind="std-GWM"
    # )

    # DefaultTreeViewStyleManager.apply_style(pjtStd_matching_treeview.treeview.tree)
    # pjtStd_matching_treeview.treeview.tree.config(height=800)
    # state.pjtStd_matching_treeview_GWM = pjtStd_matching_treeview

    # std_matching_btn_area = ttk.Frame(
    #     section2,
    #     width=100,
    # )
    # std_matching_btn_area.pack(side="top", padx=5, pady=5, anchor="ne")
    # # Create a button and place it in the window
    # add_button = tk.Button(
    #     std_matching_btn_area,
    #     text="Add 🡇",  # Button text
    #     command=lambda: handle_add_button_press(
    #         state,
    #         # data_kind="std-GWM",
    #         related_widget=pjtStdGWM_treeview,
    #     ),  # Function to call when clicked
    #     font=("Arial", 10),  # Custom font for button text
    #     bg="#fffec0",  # Background color
    #     fg="black",  # Text color
    #     width=8,  # Width of the button
    #     height=1,  # Height of the button
    #     relief=tk.RAISED,
    # )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE

    # # state.std_matching_add_btn = add_button

    # # Create a button and place it in the window
    # del_button = tk.Button(
    #     std_matching_btn_area,
    #     text="Del 🡅",  # Button text
    #     command=lambda: handle_del_button_press(
    #         state,
    #         # data_kind="std-GWM",
    #         related_widget=pjtStdGWM_treeview,
    #     ),  # Function to call when clicked
    #     font=("Arial", 10),  # Custom font for button text
    #     bg="#fffec0",  # Background color
    #     fg="black",  # Text color
    #     width=8,  # Width of the button
    #     height=1,  # Height of the button
    #     relief=tk.RAISED,
    # )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE
    # del_button.pack(
    #     side="left", padx=5, pady=5, anchor="nw"
    # )  # Add padding around the button
    # add_button.pack(
    #     side="left", padx=5, pady=5, anchor="nw"
    # )  # Add padding around the button

    # # print(state.std_edit_mode)

    # ##############################################################
    # ## section 3###########

    # WMs_sheet = TeamStd_WMsSheetView(state, section3)

    # Register widgets with EditModeManager
    edit_mode_manager.register_widgets(
        mode_button=edit_mode_button,
        tree_views=[
            pjtStdGWM_treeview,
            # pjtStd_matching_treeview,
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


def create_pjtStdSWM_tab(state, subtab_notebook):
    edit_mode_manager = EditModeManager()

    working_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(working_tab, text="Standard Work Master : Single (Std S-WM)")

    working_tab_common_area = ttk.Frame(
        working_tab,
        height=10,
    )
    working_tab_common_area.pack(expand=True, fill="x")

    working_tab_paned_area = ttk.Frame(
        working_tab,
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
    section2 = ttk.Frame(
        working_tab_paned_area,
        width=600,
        height=3000,
    )
    section3 = ttk.Frame(
        working_tab_paned_area,
        width=600,
        height=3000,
    )

    working_tab_paned_window.add(section1, minsize=400)
    working_tab_paned_window.add(section2, minsize=400)
    working_tab_paned_window.add(section3, minsize=600)

    working_tab_paned_window.paneconfigure(section1, height=3000)
    working_tab_paned_window.paneconfigure(section2, width=600, height=3000)
    working_tab_paned_window.paneconfigure(section3, height=3000)

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
    mode_button = tk.Button(
        working_tab_common_area,
        text="Locked Mode",
        command=lambda: edit_mode_manager.set_edit_mode(
            "edit" if mode_button.cget("text") == "Locked Mode" else "locked"
        ),
    )
    mode_button.pack(anchor="w", pady=5)

    ##############################################################
    ## section 1###########
    pjtStdSWM_treeview = TeamStd_SWMTreeView(state, section1)
    DefaultTreeViewStyleManager.apply_style(pjtStdSWM_treeview.treeview.tree)

    ##############################################################
    ## section 2###########
    seleted_item_label_area = ttk.Frame(
        section2,
        width=600,
    )
    seleted_item_label_area.pack(side=tk.TOP, anchor="w")

    seleted_item_label = ttk.Label(
        seleted_item_label_area,
        text="Selected Item: ",
        font=working_tab_font,
    )
    seleted_item = ttk.Label(
        seleted_item_label_area,
        # textvariable=state.selected_stdGWM_item,
        textvariable=pjtStdSWM_treeview.selected_item,
        font=working_tab_font,
        foreground="blue",
    )
    seleted_item_label.pack(side="left", padx=5, pady=5, anchor="w")
    seleted_item.pack(side="left", padx=5, pady=5, anchor="w")

    std_matching_widget_area = ttk.Frame(
        section2,
        width=600,
    )

    pjtStd_matching_treeview = TeamStd_WMmatching_TreeView(
        state, std_matching_widget_area, pjtStdSWM_treeview, data_kind="std-SWM"
    )
    DefaultTreeViewStyleManager.apply_style(pjtStd_matching_treeview.treeview.tree)
    pjtStd_matching_treeview.treeview.tree.config(height=800)
    state.pjtStd_matching_treeview_SWM = pjtStd_matching_treeview

    std_matching_btn_area = ttk.Frame(
        section2,
        width=100,
    )
    std_matching_btn_area.pack(side="top", padx=5, pady=5, anchor="ne")
    std_matching_widget_area.pack(side="top", anchor="w")
    # Create a button and place it in the window
    add_button = tk.Button(
        std_matching_btn_area,
        text="Add 🡇",  # Button text
        command=lambda: handle_add_button_press(
            state,
            # data_kind="std-SWM",
            related_widget=pjtStdSWM_treeview,
        ),  # Function to call when clicked
        font=("Arial", 10),  # Custom font for button text
        bg="#fffec0",  # Background color
        fg="black",  # Text color
        width=8,  # Width of the button
        height=1,  # Height of the button
        relief=tk.RAISED,
    )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE

    # state.std_matching_add_btn = add_button

    # Create a button and place it in the window
    del_button = tk.Button(
        std_matching_btn_area,
        text="Del 🡅",  # Button text
        command=lambda: handle_del_button_press(
            state,
            # data_kind="std-SWM",
            related_widget=pjtStdSWM_treeview,
        ),  # Function to call when clicked
        font=("Arial", 10),  # Custom font for button text
        bg="#fffec0",  # Background color
        fg="black",  # Text color
        width=8,  # Width of the button
        height=1,  # Height of the button
        relief=tk.RAISED,
    )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE
    del_button.pack(
        side="left", padx=5, pady=5, anchor="nw"
    )  # Add padding around the button
    add_button.pack(
        side="left", padx=5, pady=5, anchor="nw"
    )  # Add padding around the button
    # state.std_matching_del_btn = del_button

    # print(state.std_edit_mode)

    ##############################################################
    ## section 3###########

    WMs_inSWM_sheet = TeamStd_WMsSheetView(state, section3)

    # Register widgets with EditModeManager
    edit_mode_manager.register_widgets(
        mode_button=mode_button,
        tree_views=[
            pjtStdSWM_treeview,
            pjtStd_matching_treeview,
        ],
        tree_ctrl_btn=[
            add_button,
            del_button,
        ],
        sheet=WMs_inSWM_sheet,
    )

    # Set the initial state to "Locked Mode"
    edit_mode_manager.set_edit_mode("locked")

    return working_tab