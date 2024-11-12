import tkinter as tk
import tkinter.font
from tkinter import ttk

from src.models.sheet_utils import parse_Json_toSheet
from src.controllers.tksheet.sheet_utils import (
    on_paste_cells,
    on_sheet_data_change,
)
from src.views.tksheet.sheet_utils import (
    add_edit_mode_radio_buttons,
    create_tksheet,
    on_cell_select_stdGWMsheet,
)


def create_stdGWM_tab(state, subtab_notebook):
    stdGWM_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(stdGWM_tab, text="Standard Work Master : Group (G-WM)")

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
    sheet_label = tk.Label(
        tab_common_area,
        text="Group Work Master",
        font=stdGWM_tab_font,
        # width=10,
        # height=5,
    )
    sheet_label.pack(padx=5, pady=5, anchor="w")

    # Place tksheet in G-WM tab

    stdGWM_sheet = create_tksheet(
        state,
        section1,
        headers=state.stdGWM_headers,
        data=[
            ["", ""],
        ],
        # * 100,
        tab_name=None,
        height=2000,
        width=400,
        mode=None,
        select_bindFunc=on_cell_select_stdGWMsheet,
    )

    add_edit_mode_radio_buttons(state, stdGWM_sheet, section1)

    stdGWM_sheet["B"].highlight(fg="purple")
    stdGWM_sheet["C"].highlight(fg="blue")

    stdGWM_sheet.kind = "std-GWM"
    stdGWM_sheet.pack(padx=5, pady=2, anchor="w")

    # 칼럼 폭 자동 맞춤
    # auto_adjust_all_column_widths(stdGWM_sheet)
    stdGWM_sheet.set_options(auto_resize_columns=50)

    # tksheet의 셀 데이터 변경 이벤트 바인딩
    stdGWM_sheet.extra_bindings(
        [
            ("end_edit_cell", lambda e: on_sheet_data_change(e, state, stdGWM_sheet)),
            ("begin_paste", lambda e: on_paste_cells(e, state, stdGWM_sheet)),
            ("end_paste", lambda e: on_sheet_data_change(e, state, stdGWM_sheet)),
        ]
    )

    def update_stdGWM_sheet(e, state, sheet):
        # 상태 변경 시 tksheet를 업데이트
        data_forSheet = parse_Json_toSheet(
            state.team_std_info["std-GWM"], mode="std-GWM"
        )
        sheet.set_sheet_data(
            data_forSheet,
            # reset_col_positions=True,
            # reset_row_positions=True,
        )

    # 옵저버 함수 등록
    state.observer_manager.add_observer(
        lambda e: update_stdGWM_sheet(e, state, stdGWM_sheet)
    )

    ## section 2
    seleted_item_label_area = ttk.Frame(
        section2,
        width=1000,
    )
    seleted_item_label_area.pack(anchor="w")

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

    return stdGWM_tab
