import tkinter as tk
import tkinter.font
from tkinter import ttk

# from src.controllers.widget.sheet_utils import (
#     on_paste_cells,
#     on_stdGWM_sheet_data_change,
# )
from src.views.widget.sheet_utils import (
    # add_edit_mode_radio_buttons,
    create_tksheet,
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
        height=50,
    )
    tab_common_area.pack(expand=True, fill="x")

    stdGWM_tab_paned_area = ttk.Frame(
        stdGWM_tab,
        # width=600,
        height=2000,
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
        width=400,
        height=2000,
    )
    section2 = ttk.Frame(
        stdGWM_tab_paned_area,
        width=800,
        height=2000,
    )
    section3 = ttk.Frame(
        stdGWM_tab_paned_area,
        width=800,
        height=2000,
    )

    stdGWM_tab_paned_window.add(section1)
    stdGWM_tab_paned_window.add(section2)
    stdGWM_tab_paned_window.add(section3)
    stdGWM_tab_paned_window.paneconfigure(section2, width=600)

    # common 영역 라벨링
    stdGWM_tab_font = tk.font.Font(
        family="맑은 고딕",
        size=12,
        # weight="bold",
    )

    # Place tksheet in G-WM tab

    # stdGWM_sheet = create_tksheet(
    #     state,
    #     section1,
    #     headers=state.stdGWM_headers,
    #     data=[
    #         ["", ""],
    #     ],
    #     tab_name=None,
    #     height=2000,
    #     width=400,
    #     mode=None,
    #     select_bindFunc=on_cell_select_stdGWMsheet,
    # )

    # stdGWM_sheet["B"].highlight(fg="purple")
    # stdGWM_sheet["C"].highlight(fg="blue")

    # stdGWM_sheet.kind = "std-GWM"

    # # 칼럼 폭 자동 맞춤
    # stdGWM_sheet.set_options(auto_resize_columns=50)

    # # tksheet의 셀 데이터 변경 이벤트 바인딩
    # stdGWM_sheet.extra_bindings(
    #     [
    #         (
    #             "end_edit_cell",
    #             lambda e: on_stdGWM_sheet_data_change(e, state, stdGWM_sheet),
    #         ),
    #         (
    #             "begin_paste",
    #             lambda e: on_paste_cells(e, state, stdGWM_sheet),
    #         ),
    #         (
    #             "end_paste",
    #             lambda e: on_stdGWM_sheet_data_change(e, state, stdGWM_sheet),
    #         ),
    #     ]
    # )
    # state.stdGWM_sheet = stdGWM_sheet

    stdGWM_treeview = TeamStd_GWMTreeView(state, section1)
    DefaultTreeViewStyleManager.apply_style(stdGWM_treeview.treeview.tree)

    ##############################################################
    ## section 2###########
    seleted_item_label_area = ttk.Frame(
        section2,
        width=1000,
    )
    seleted_item_label_area.pack(side=tk.TOP, anchor="w")

    seleted_item_label = tk.Label(
        seleted_item_label_area,
        text="Selected Item: ",
        font=stdGWM_tab_font,
        # width=10,
        # height=5,
    )
    seleted_item = tk.Label(
        seleted_item_label_area,
        textvariable=state.selected_stdGWM_item,
        font=stdGWM_tab_font,
        fg="blue",
        # width=10,
        # height=5,
    )
    seleted_item_label.pack(side="left", padx=5, pady=5, anchor="w")
    seleted_item.pack(side="left", padx=5, pady=5, anchor="w")

    std_matching_listbox_area = ttk.Frame(
        section2,
        width=1500,
    )
    std_matching_listbox_area.pack(side=tk.LEFT, anchor="w")

    # std_matching_listbox = create_listbox(state, std_matching_listbox_area)
    # state.std_matching_listbox = std_matching_listbox

    std_matching_treeview = TeamStd_GWMmatching_TreeView(
        state, std_matching_listbox_area
    )
    DefaultTreeViewStyleManager.apply_style(std_matching_treeview.treeview.tree)

    std_matching_btn_area = ttk.Frame(
        std_matching_listbox_area,
        # width=100,
    )
    std_matching_btn_area.pack(side="left", padx=5, pady=5, anchor="nw")

    # Create a button and place it in the window
    add_button = tk.Button(
        std_matching_btn_area,
        text="Add",  # Button text
        command=lambda x: x,  # Function to call when clicked
        font=("Arial", 10),  # Custom font for button text
        bg="#fffec0",  # Background color
        fg="black",  # Text color
        width=8,  # Width of the button
        height=1,  # Height of the button
        relief=tk.RAISED,
    )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE
    add_button.pack(
        side="top", padx=5, pady=5, anchor="nw"
    )  # Add padding around the button
    state.std_matching_add_btn = add_button

    # Create a button and place it in the window
    del_button = tk.Button(
        std_matching_btn_area,
        text="Del",  # Button text
        command=lambda x: x,  # Function to call when clicked
        font=("Arial", 10),  # Custom font for button text
        bg="#fffec0",  # Background color
        fg="black",  # Text color
        width=8,  # Width of the button
        height=1,  # Height of the button
        relief=tk.RAISED,
    )  # Border style: can be FLAT, SUNKEN, RAISED, GROOVE, RIDGE
    del_button.pack(
        side="top", padx=5, pady=5, anchor="nw"
    )  # Add padding around the button
    state.std_matching_del_btn = del_button

    # print(state.std_edit_mode)

    ##############################################################
    ## section 3###########
    WMs_sheet = create_tksheet(
        state,
        section3,
        # headers=state.stdGWM_headers,
        data=[],
        tab_name=None,
        height=2000,
        width=1000,
        mode=None,
        # select_bindFunc=on_cell_select_stdGWMsheet,
    )
    WMs_sheet.kind = "WMs"

    # 칼럼 폭 자동 맞춤
    # WMs_sheet.set_options(auto_resize_columns=100)
    WMs_sheet.set_all_cell_sizes_to_text(width=5, slim=True)
    WMs_sheet.pack(padx=5, pady=2, anchor="w")

    ####################################################################
    ####################################################################
    ####################################################################
    ####################################################################
    ####################################################################

    # # 옵저버 함수 등록
    # state.observer_manager.add_observer(
    #     lambda e: updateWidget_stdGWM_sheet(e, state, stdGWM_sheet),
    # )
    # 옵저버 함수 등록
    state.observer_manager.add_observer(
        lambda e: updateWidget_WMs_sheet(e, state, WMs_sheet),
    )

    # add_edit_mode_radio_buttons(state, stdGWM_sheet, section1)
    # stdGWM_sheet.pack(padx=5, pady=2, anchor="w")

    return stdGWM_tab
