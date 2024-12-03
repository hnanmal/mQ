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
    TeamStd_GWMmatching_TreeView,
    TeamStd_WMmatching_TreeView,
    TeamStd_SWMTreeView,
)
from src.views.widget.widget import WidgetSwitcher


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
        width=400,
        height=3000,
    )
    section3 = ttk.Frame(
        working_tab_paned_area,
        width=600,
        height=3000,
    )

    working_tab_paned_window.add(section2, minsize=300)
    working_tab_paned_window.add(section1, minsize=400)
    working_tab_paned_window.add(section3, minsize=800)

    working_tab_paned_window.paneconfigure(section1, width=1200, height=3000)
    working_tab_paned_window.paneconfigure(section2, width=300, height=3000)
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
    stdFamlist_treeview = TeamStd_FamlistTreeView(state, section1, view_level=3)
    DefaultTreeViewStyleManager.apply_style(stdFamlist_treeview.treeview.tree)
    stdFamlist_treeview.treeview.tree.column(0, width=0, minwidth=0, stretch=False)

    # stdFamlist_treeview2 = TeamStd_WMsSheetView(state, section2)

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
        textvariable=stdFamlist_treeview.selected_item,
        font=working_tab_font,
        foreground="blue",
    )
    selected_item_label.pack(side="left", padx=5, pady=5, anchor="w")
    selected_item.pack(side="left", padx=5, pady=5, anchor="w")

    std_matching_widget_area = ttk.Frame(
        section2,
        width=600,
    )

    std_GWMTreeView = TeamStd_GWMTreeView(state, std_matching_widget_area, view_level=1)
    # std_GWMTreeView.treeview.tree.column(2, width=0, minwidth=0, stretch=False)
    std_GWMTreeView.tree_frame.pack_forget()

    std_SWMTreeView = TeamStd_SWMTreeView(state, std_matching_widget_area, view_level=1)
    # std_SWMTreeView.treeview.tree.column(2, width=0, minwidth=0, stretch=False)
    std_SWMTreeView.tree_frame.pack_forget()

    # std_GWMTreeView.tree_frame.pack(
    #     side="left",
    #     padx=20,
    #     pady=5,
    # )
    # std_SWMTreeView.tree_frame.pack(
    #     side="left",
    #     padx=10,
    #     pady=5,
    # )

    widgetSwitcher = WidgetSwitcher(
        std_matching_widget_area,
        {
            "GWM": std_GWMTreeView.tree_frame,
            "SWM": std_SWMTreeView.tree_frame,
        },
        default_selection="GWM",
        default_width=600,
    )

    std_matching_btn_area = ttk.Frame(
        section2,
        width=100,
    )
    std_matching_btn_area.pack(side="top", padx=5, pady=5, anchor="ne")
    std_matching_widget_area.pack(side="top", anchor="w")
    # Create a button and place it in the window
    add_button = tk.Button(
        std_matching_btn_area,
        text="Add ⇨",  # Button text
        command=lambda: handle_add_button_press(
            state,
            # data_kind="std-GWM",
            related_widget=stdFamlist_treeview,
        ),  # Function to call when clicked
        font=("Arial", 10),  # Custom font for button text
        bg="#fffec0",  # Background color
        fg="black",  # Text color
        width=8,  # Width of the button
        height=1,  # Height of the button
        relief=tk.RAISED,
    )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE

    # # Create a button and place it in the window
    # del_button = tk.Button(
    #     std_matching_btn_area,
    #     text="Del 🡅",  # Button text
    #     command=lambda: handle_del_button_press(
    #         state,
    #         # data_kind="std-GWM",
    #         related_widget=stdFamlist_treeview,
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
    add_button.pack(
        side="left", padx=5, pady=5, anchor="nw"
    )  # Add padding around the button

    ##############################################################
    ## section 3###########

    # std_GWMTreeView.treeview.toggle_tree_lock(lock=True)
    # std_GWMTreeView.treeview.expand_tree_to_level(level=1)
    stdGWMmatching_treeview = TeamStd_GWMmatching_TreeView(
        state, section3, stdFamlist_treeview
    )
    # Register widgets with EditModeManager
    edit_mode_manager.register_widgets(
        mode_button=edit_mode_button,
        tree_views=[
            stdFamlist_treeview,
            stdGWMmatching_treeview,
            std_GWMTreeView,
            std_SWMTreeView,
        ],
        tree_ctrl_btn=[
            add_button,
            # del_button,
        ],
        # sheet=WMs_sheet,
    )

    # Set the initial state to "Locked Mode"
    edit_mode_manager.set_edit_mode("locked")

    return working_tab
