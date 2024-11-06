from src.core.fp_utils import *
from src.views.tksheet.sheet_utils import parse_sheet_toJson


# tksheet 데이터가 변경될 때 호출되는 콜백 정의 (이 위치에 배치)
def on_sheet_data_change(event, state, sheet):

    print("on_sheet_data_change_start")

    sheet_headers = sheet.headers()
    # print("sheet_headers", sheet_headers)

    # Get all data from tksheet
    new_data_ = sheet.get_sheet_data()
    # print(new_data_)
    new_data = parse_sheet_toJson(sheet)
    # for dat in new_data:
    #     pass

    # Update the state with new data
    state.update_S_GWM_data(new_data)
    print("on_sheet_data_change_end")

    # print("dd", state.project_info)


def on_paste_cells(event, state, sheet):
    print("on_paste_cells_start")
    # Get the data being pasted
    # paste_data = sheet.clipboard_get()
    paste_data = sheet.clipboard_get().split("\n")
    # sheet.paste()
    # This method will get the data from the clipboard
    # print("paste_data -", paste_data)
    # print("paste_data :", type(paste_data), len(paste_data))

    current_data = sheet.get_sheet_data()
    rows_needed = len(paste_data) - len(current_data)
    print("rows_needed", rows_needed)
    if rows_needed > 0:
        # Add rows if there are not enough rows for the paste
        sheet.insert_rows(rows=rows_needed)
        # for _ in range(rows_needed):
        #     sheet.insert_rows(rows=len(current_data))
    # Proceed with the paste operation
    # sheet.paste()  # Perform the actual paste

    print("on_paste_cells_end")

    # on_sheet_data_change(None, state, sheet)
