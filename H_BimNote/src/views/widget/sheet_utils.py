# src/views/widget/sheet_utils.py

import tkinter as tk
from tkinter import ttk
from tksheet import Sheet

from src.models.sheet_utils import parse_DB_toSheet
from src.controllers.widget.widgets import toggle_stdGWM_widget_mode


def updateWidget_stdGWM_sheet(event, state, sheet):
    # 상태 변경 시 tksheet를 업데이트
    data_forSheet = parse_DB_toSheet(state.team_std_info["std-GWM"], mode="std-GWM")
    sheet.set_sheet_data(
        data_forSheet,
        # reset_col_positions=True,
        # reset_row_positions=True,
    )


def updateWidget_WMs_sheet(event, state, sheet):
    # Updating tksheet in the UI
    data_forSheet = state.team_std_info["WMs"]
    sheet.set_sheet_data(data_forSheet)


def updateWidget_matching_listbox(event, state, listbox):
    pass


def on_cell_select(event, state, sheet, color="#fffec0"):
    # 선택된 셀의 위치 가져오기
    selected_cells = list(sheet.get_selected_cells())

    if selected_cells:
        # 기존 스타일 초기화
        sheet.dehighlight_rows()

        # 선택된 행 강조 표시 (예: 노란색으로 설정)
        selected_rows = list(map(lambda x: x[0], selected_cells))
        print(selected_rows)

        sheet.highlight_rows(
            rows=selected_rows, bg=color, fg="black", highlight_index=True
        )

    state.log_widget.write(
        f"선택 발생! 외애애애애애엥 [{sheet.kind}]시트, [{selected_cells}] 에서 선택 발생!!!!"
    )


def on_cell_select_stdGWMsheet(event, state, sheet):
    on_cell_select(event, state, sheet, color="yellow")

    selected_cells = list(sheet.get_selected_cells())

    def find_GWM(sheet, selected_row):
        crnt_row = selected_row
        if sheet.get_cell_data(crnt_row, 1):
            return sheet.get_cell_data(crnt_row, 1)
        else:
            return find_GWM(sheet, crnt_row - 1)

    def find_class(sheet, selected_row):
        crnt_row = selected_row
        if sheet.get_cell_data(crnt_row, 0):
            return sheet.get_cell_data(crnt_row, 0)
        else:
            return find_class(sheet, crnt_row - 1)

    if selected_cells:
        selected_row = selected_cells[0][0]
        if sheet.get_cell_data(selected_row, 2):
            parent_class = find_class(sheet, selected_row)
            parent_GWM = find_GWM(sheet, selected_row)
            res = f"{parent_class} | {parent_GWM} | {sheet.get_cell_data(selected_row, 2)}"
            state.selected_stdGWM_item.set(res)
        else:
            sheet.dehighlight_rows()
            state.selected_stdGWM_item.set(None)


def create_tksheet(
    state,
    frame,
    headers=[],
    data=[],
    tab_name=None,
    height=None,
    width=None,
    mode=None,
    select_bindFunc=None,
):

    sheet = Sheet(frame, headers=headers, height=height, width=width)

    sheet.enable_bindings(
        "edit_cell",
        "delete",
        "single_select",  # Allow single cell selection
        "drag_select",
        "row_select",  # Allow row selection
        "column_select",  # Allow column selection
        "drag_select",  # Allow drag selection
        "column_width_resize",
        "row_height_resize",
        "double_click_column_resize",
        "copy",
        "paste",
        "ctrl_click_select",
        "right_click_popup_menu",
        "rc_insert_row",
        "rc_delete_row",
        "arrowkeys",
    )
    sheet.header_font(("Arial", 8, "normal"))
    sheet.set_options(
        font=("Arial Narrow", 10, "normal"), default_row_height=35
    )  # Font name and size

    if select_bindFunc:
        sheet.extra_bindings(
            [
                ("cell_select", lambda e: select_bindFunc(e, state, sheet)),
            ]
        )
    else:
        sheet.extra_bindings(
            [
                ("drag_select_cells", lambda e: on_cell_select(e, state, sheet)),
            ]
        )

    sheet.set_sheet_data(data)
    sheet.kind = None

    return sheet


def add_edit_mode_radio_buttons(state, sheet, parent_frame):
    """편집 모드 전환 라디오 버튼을 추가하는 함수"""
    # edit_mode = tk.StringVar(value="locked")  # 기본은 잠금 모드로 설정

    frame = tk.Frame(parent_frame)
    frame.pack(anchor="w")

    # 라디오 버튼 생성 및 배치
    radio_locked = ttk.Radiobutton(
        frame,
        text="Locked Mode",
        variable=state.std_edit_mode,
        value="locked",
        command=lambda: toggle_stdGWM_widget_mode(state, sheet, state.std_edit_mode),
    )

    radio_edit = ttk.Radiobutton(
        frame,
        text="Edit Mode",
        variable=state.std_edit_mode,
        value="edit",
        command=lambda: toggle_stdGWM_widget_mode(state, sheet, state.std_edit_mode),
    )

    radio_locked.pack(side="left", padx=10, pady=10)
    radio_edit.pack(side="left", padx=10, pady=10)
    # radio_locked.select()

    # 초기 상태를 라디오 버튼의 값에 맞춰서 설정
    toggle_stdGWM_widget_mode(state, sheet, state.std_edit_mode)


def populate_tksheet(state, sheet):
    pass
