from src.models.sheet_utils import parse_sheet_toJson
from src.core.fp_utils import *


# tksheet 데이터가 변경될 때 호출되는 콜백 정의 (이 위치에 배치)
def on_sheet_data_change(event, state, sheet):

    print("on_sheet_data_change_start")

    # Get all data from tksheet
    new_data = parse_sheet_toJson(sheet)

    # Update the state with new data
    state.updateDB_S_GWM_data(new_data)
    print("on_sheet_data_change_end")


def on_paste_cells(event, state, sheet):
    print("on_paste_cells_start")
    # Get the data being pasted
    paste_data = sheet.clipboard_get().split("\n")

    # This method will get the data from the clipboard
    current_data = sheet.get_sheet_data()
    rows_needed = len(paste_data) - len(current_data)
    print("rows_needed", rows_needed)
    if rows_needed > 0:
        # Add rows if there are not enough rows for the paste
        sheet.insert_rows(rows=rows_needed)

    print("on_paste_cells_end")

    # on_sheet_data_change(None, state, sheet)


def toggle_sheet_mode(state, sheet, edit_mode_var):
    """시트의 편집 가능 여부를 전환하는 함수"""
    mode = edit_mode_var.get()
    if mode == "edit":
        sheet.enable_bindings()  # 모든 기본 바인딩 활성화
        state.log_widget.write("Sheet is now in Edit Mode")
    elif mode == "locked":
        # 편집 관련 바인딩을 비활성화하여 편집을 잠금
        sheet.disable_bindings(
            "edit_cell",
            "delete",
            "insert_row",
            "delete_row",
            "paste",
        )
        state.log_widget.write("Sheet is now in Locked Mode")
