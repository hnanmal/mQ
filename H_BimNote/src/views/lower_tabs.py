import tkinter as tk
from tkinter import ttk

from src.controllers.tksheet.sheet_utils import on_paste_cells, on_sheet_data_change
from src.views.tksheet.sheet_utils import create_tksheet


def create_wmGrp_tab(state, subtab_notebook):
    g_wm_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(g_wm_tab, text="Standard Work Master Group (G-WM)")

    paned_window = tk.PanedWindow(
        g_wm_tab,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    paned_window.pack(expand=True, fill="both")

    section1 = ttk.Frame(
        g_wm_tab,
        width=700,
        height=2000,
    )

    section2 = ttk.Frame(
        g_wm_tab,
        width=700,
        height=2000,
    )

    paned_window.add(section1)
    paned_window.add(section2)

    # Place tksheet in G-WM tab
    S_GWM_sheet = create_tksheet(
        state,
        section1,
        headers=state.GWM_headers,
        data=[
            ["", ""],
        ],
        # * 100,
        tab_name=None,
        height=2000,
        width=600,
        mode=None,
    )
    S_GWM_sheet.kind = "GWM"
    S_GWM_sheet.pack(padx=5, pady=2, anchor="w")

    # tksheet의 셀 데이터 변경 이벤트 바인딩
    S_GWM_sheet.extra_bindings(
        [
            ("end_edit_cell", lambda e: on_sheet_data_change(e, state, S_GWM_sheet)),
            ("begin_paste", lambda e: on_paste_cells(e, state, S_GWM_sheet)),
            ("end_paste", lambda e: on_sheet_data_change(e, state, S_GWM_sheet)),
        ]
    )

    def update_sheet(e, state, sheet):
        # 상태 변경 시 tksheet를 업데이트
        sheet.set_sheet_data(
            state.team_std_info["GWM"],
            # reset_col_positions=True,
            # reset_row_positions=True,
        )

    # 옵저버 함수 등록
    state.observer_manager.add_observer(lambda e: update_sheet(e, state, S_GWM_sheet))

    # Place tksheet in G-WM tab
    sheet2 = create_tksheet(
        state,
        section2,
        headers=state.GWM_headers,
        data=[
            [1, 32],
            [1, 32],
        ],
        tab_name=None,
        height=2000,
        width=600,
        mode=None,
    )

    sheet2.pack(padx=5, pady=2, anchor="w")

    return g_wm_tab
