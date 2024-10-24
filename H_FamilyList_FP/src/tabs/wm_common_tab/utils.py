from src.utils.fp_utils import *

import tkinter as tk
from tkinter import ttk
from tksheet import Sheet
from copy import copy


# Function to update the second cell dropdown (B1) based on the first cell selection
def update_second_cell_dropdown_allCat(event, state, sheet):
    all_row_index = list(range(sheet.get_total_rows()))
    # print(all_row_index)

    # print(second_dropdowns)
    # Set the second cell's dropdown based on the first cell's value
    WM_col_idx = 4
    unit_col_idx = 2
    wmGrp_col_idx = 1
    class_col_idx = 0
    desc_col_idx = WM_col_idx + 1

    def update_unitCell_inRow(row_idx):
        if sheet.get_cell_data(row_idx, WM_col_idx):
            selected_value = sheet.get_cell_data(row_idx, WM_col_idx)
            unit_info = selected_value.split(" | ")[-4]
            sheet.set_cell_data(row_idx, unit_col_idx, unit_info)

    def update_descriptionCell_inRow(row_idx):
        if sheet.get_cell_data(row_idx, WM_col_idx):
            selected_value = sheet.get_cell_data(row_idx, WM_col_idx)
            desc_info_list = go(
                selected_value.split(" | "),
                # filter(lambda x: ("(   )" in x) or ("(  )" in x)),
                filter(
                    lambda x: ("(   )" in x) or ("(   )" in x) or ("(  )" in x)
                ),  # 가운데 조건이 공백특수문자인듯?
                list,
            )
            desc_info = "\n".join(desc_info_list)
            sheet.set_cell_data(row_idx, desc_col_idx, desc_info)

    def update_row(row_idx):
        sheet.del_dropdown(row_idx, WM_col_idx)
        selected_value = sheet.get_cell_data(row_idx, wmGrp_col_idx)
        # print(type(selected_value))
        # print(selected_value)
        try:
            current_WM_value = copy(
                sheet.get_cell_data(row_idx, WM_col_idx)
            )  # Get selected value from the first cell
        except:
            current_WM_value = None
        # print(current_WM_value)
        second_dropdowns_obj = state.wm_group_data.get(
            selected_value, {"matched_items": []}
        )
        # print(second_dropdowns_obj)

        second_dropdowns = go(
            second_dropdowns_obj["matched_items"],
            map(lambda x: x.split(" | ")),
            map(lambda x: filter(lambda y: y != "0", x)),
            map(lambda x: filter(lambda y: y != "", x)),
            map(lambda x: " | ".join(x)),
            list,
        )
        if sheet.get_cell_data(row_idx, class_col_idx) == "":
            sheet.dehighlight_rows(row_idx)
            if not current_WM_value:
                sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
                update_unitCell_inRow(idx)
                update_descriptionCell_inRow(idx)
            elif current_WM_value == second_dropdowns_obj["matched_items"][0]:
                # second_dropdowns = second_dropdowns_obj["matched_items"]
                sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
            elif current_WM_value != second_dropdowns_obj["matched_items"][0]:
                # second_dropdowns = second_dropdowns_obj["matched_items"]
                sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
                sheet.set_cell_data(row_idx, WM_col_idx, current_WM_value)
            elif current_WM_value not in second_dropdowns_obj["matched_items"]:
                # second_dropdowns = second_dropdowns_obj["matched_items"]
                sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
                # sheet.set_cell_data(idx, 4, current_WM_value)
            else:
                pass
        else:
            sheet.highlight_rows(row_idx, bg="#f9edff", fg="blue")
        #     sheet.del_dropdown(idx, class_col_idx)

    for idx in all_row_index:
        update_row(idx)
        # update_unitCell_inRow(idx)
        # update_descriptionCell_inRow(idx)

    sheet.set_column_widths(state.wmCat_col_widths)
    sheet.set_all_row_heights(state.wmCat_row_heights)
    # sheet.see(column=0)


def on_select_wmCatCombo(event, state):
    sheet = state.commonWM_sheet
    all_row_index = list(range(sheet.get_total_rows()))

    sheet.dehighlight_rows(all_row_index)
    # sheet.delete_dropdown("E")
    # print(dir(sheet))

    selected_kind = state.wmCat_comboBox.get()

    filtered_data = go(
        state.common_wm_data,
        filter(lambda x: selected_kind in str(x)),
        # map(lambda x: ["", x]),
        list,
    )
    # print(filtered_data)

    grp_names = {
        "RC공통": [
            "콘크리트",
            "거푸집",
            "철근",
            "차단층",
            "단열층",
            "그라우트",
            "데크",
            "토공",
        ],
        "철골공통": [
            "-Heavy",
            "-Medium",
            "-Light",
            "-Extra Heavy",
            "-Extra Light",
            "거스퍼린",
            "플레이트",
            "철골도장",
            "철골계단",
            "핸드레일",
        ],
        "조적공통": [
            "블록층",
            "조적층",
            "플라스터",
        ],
        "마감공통": [
            "샌드위치패널",
            "싱글시트",
            "거터",
        ],
    }

    grped_data = []
    for grp_name in grp_names[selected_kind]:
        grped_data.append(["[" + grp_name + "]"])
        tmp = []
        if grp_name != "토공":
            for i in filtered_data:
                if grp_name in i[1]:
                    tmp.append(i)
            grped_data.extend(sorted(tmp))
        else:
            for i in filtered_data:
                if (
                    "터파기" in i[1]
                    or "되메우기" in i[1]
                    or "잔토처리" in i[1]
                    or "기층" in i[1]
                ):
                    tmp.append(i)
            grped_data.extend(sorted(tmp))

    # sheet.set_sheet_data(filtered_data)
    sheet.set_sheet_data(grped_data)
    sheet.set_column_widths(state.wmCat_col_widths)
    sheet.set_all_row_heights(state.wmCat_row_heights)

    for row_idx in all_row_index:
        if sheet.get_cell_data(row_idx, 0) == "":
            sheet.dehighlight_rows([row_idx])
        else:
            sheet.highlight_rows([row_idx], bg="#f9edff", fg="blue")

    # sheet.see(column=0)


def create_tksheet_commonWM(
    state, frame, headers=[], data=[], tab_name=None, height=None, width=None, mode=None
):

    sheet = Sheet(frame, headers=headers, height=height, width=width)
    sheet.enable_bindings(
        "edit_cell",
        # "delete",
        "single_select",  # Allow single cell selection
        "drag_select",
        "row_select",  # Allow row selection
        "column_select",  # Allow column selection
        "drag_select",  # Allow drag selection
        "column_width_resize",
        "double_click_column_resize",
        "copy",
        "ctrl_click_select",
        "right_click_popup_menu",
        # "rc_insert_row",
        # "rc_delete_row",
        "arrowkeys",
    )
    sheet.header_font(("Arial", 8, "normal"))
    sheet.set_options(font=("Arial Narrow", 9, "normal"))  # Font name and size

    sheet.set_sheet_data(data)
    sheet.set_column_widths(state.wmCat_col_widths)
    sheet.set_all_row_heights(state.wmCat_row_heights)
    sheet.see(column=0)

    sheet.extra_bindings(
        [
            # (
            #     "rc_insert_row",
            #     lambda e: add_assignRow_allCat(e, state, sheet, tab_name=tab_name),
            # ),
            # (
            #     "rc_delete_row",
            #     lambda e: on_change_wmSheet_allCat(
            #         e, state, sheet, tab_name, mode="stdType"
            #     ),
            # ),
            # (
            #     "end_edit_cell",
            #     # lambda e: update_second_cell_dropdown(e, state, sheet),
            #     lambda e: on_change_wmSheet_allCat(
            #         e, state, sheet, tab_name, mode="stdType"
            #     ),
            # ),
            (
                "cell_select",
                lambda e: update_second_cell_dropdown_allCat(e, state, sheet),
            ),
        ]
    )

    return sheet
