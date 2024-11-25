import tkinter as tk
import tkinter.font
from tkinter import ttk

# from src.controllers.widget.sheet_utils import (
#     on_paste_cells,
#     on_stdGWM_sheet_data_change,
# )
from src.controllers.widget.widgets import (
    handle_add_button_press,
    handle_del_button_press,
)
from src.views.widget.sheet_utils import (
    # add_edit_mode_radio_buttons,
    TeamStd_WMsSheetView,
    create_tksheet,
    on_cell_select_WMsSheet,
    # on_cell_select_stdGWMsheet,
    updateWidget_WMs_sheet,
    # updateWidget_stdGWM_sheet,
)
from src.views.widget.listbox_utils import create_listbox
from src.views.widget.treeview_utils import (
    TeamStd_GWMTreeView,
    DefaultTreeViewStyleManager,
    TeamStd_GWMmatching_TreeView,
)


def create_stdGWM_tab(state, subtab_notebook):
    stdGWM_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(stdGWM_tab, text="Standard Work Master : Group (Std G-WM)")

    tab_common_area = ttk.Frame(
        stdGWM_tab,
        # width=2000,
        height=10,
    )
    tab_common_area.pack(expand=True, fill="x")

    tmpLabel = ttk.Label(tab_common_area)

    stdGWM_tab_paned_area = ttk.Frame(
        stdGWM_tab,
        # width=600,
        height=3000,
    )
    stdGWM_tab_paned_area.pack(expand=True, fill="both")

    stdGWM_tab_paned_window = tk.PanedWindow(
        stdGWM_tab_paned_area,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    stdGWM_tab_paned_window.pack(expand=True, fill="both")

    section1 = ttk.Frame(
        stdGWM_tab_paned_area,
        width=1000,
        height=3000,
    )
    section2 = ttk.Frame(
        stdGWM_tab_paned_area,
        width=600,
        height=3000,
    )
    section3 = ttk.Frame(
        stdGWM_tab_paned_area,
        width=600,
        height=3000,
    )

    stdGWM_tab_paned_window.add(section1, minsize=400)
    stdGWM_tab_paned_window.add(section2, minsize=400)
    stdGWM_tab_paned_window.add(section3, minsize=600)

    stdGWM_tab_paned_window.paneconfigure(section1, height=3000)
    stdGWM_tab_paned_window.paneconfigure(section2, width=600, height=3000)
    stdGWM_tab_paned_window.paneconfigure(section3, height=3000)
    # stdGWM_tab_paned_window.paneconfigure(section2, width=600)

    # common 영역 라벨링
    stdGWM_tab_font = tk.font.Font(
        family="맑은 고딕",
        size=12,
        # weight="bold",
    )

    # Place tksheet in G-WM tab
    ##############################################################
    ## tab_common_area###########
    # Create an "Edit Mode" / "Locked Mode" button
    mode_button = tk.Button(
        tab_common_area,
        text="Locked Mode",
        command=lambda: state.edit_mode_manager.set_edit_mode(
            "edit" if mode_button.cget("text") == "Locked Mode" else "locked"
        ),
    )
    mode_button.pack(anchor="w", pady=5)

    ##############################################################
    ## section 1###########
    stdGWM_treeview = TeamStd_GWMTreeView(state, section1)
    DefaultTreeViewStyleManager.apply_style(stdGWM_treeview.treeview.tree)

    ##############################################################
    ## section 2###########
    seleted_item_label_area = ttk.Frame(
        section2,
        width=600,
    )
    seleted_item_label_area.pack(side=tk.TOP, anchor="w")

    seleted_item_label = tk.Label(
        seleted_item_label_area,
        text="Selected Item: ",
        font=stdGWM_tab_font,
    )
    seleted_item = tk.Label(
        seleted_item_label_area,
        textvariable=state.selected_stdGWM_item,
        font=stdGWM_tab_font,
        fg="blue",
    )
    seleted_item_label.pack(side="left", padx=5, pady=5, anchor="w")
    seleted_item.pack(side="left", padx=5, pady=5, anchor="w")

    std_matching_widget_area = ttk.Frame(
        section2,
        width=600,
    )

    std_matching_treeview = TeamStd_GWMmatching_TreeView(
        state, std_matching_widget_area
    )
    DefaultTreeViewStyleManager.apply_style(std_matching_treeview.treeview.tree)
    std_matching_treeview.treeview.tree.config(height=800)
    state.std_matching_treeview = std_matching_treeview

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
            state, mode="std_matching"
        ),  # Function to call when clicked
        font=("Arial", 10),  # Custom font for button text
        bg="#fffec0",  # Background color
        fg="black",  # Text color
        width=8,  # Width of the button
        height=1,  # Height of the button
        relief=tk.RAISED,
    )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE

    state.std_matching_add_btn = add_button

    # Create a button and place it in the window
    del_button = tk.Button(
        std_matching_btn_area,
        text="Del 🡅",  # Button text
        command=lambda: handle_del_button_press(
            state, mode="std_matching"
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
    state.std_matching_del_btn = del_button

    # print(state.std_edit_mode)

    ##############################################################
    ## section 3###########

    WMs_sheet = TeamStd_WMsSheetView(state, section3)

    # Register widgets with EditModeManager
    state.edit_mode_manager.register_widgets(
        mode_button=mode_button,
        tree_views=[
            # stdGWM_treeview,
            std_matching_treeview,
        ],
        tree_ctrl_btn=[
            add_button,
            del_button,
        ],
        sheet=WMs_sheet,
    )

    # Set the initial state to "Locked Mode"
    state.edit_mode_manager.set_edit_mode("locked")

    return stdGWM_tab
