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
    def update_unitCell_inRow(idx):
        if sheet.get_cell_data(idx, 4):
            selected_value = sheet.get_cell_data(idx, 4)
            unit_info = selected_value.split(" | ")[-4]
            sheet.set_cell_data(idx, 2, unit_info)

    def update_row(idx):
        selected_value = sheet.get_cell_data(idx, 0)
        # print(type(selected_value))
        # print(selected_value)
        try:
            current_WM_value = copy(
                sheet.get_cell_data(idx, 4)
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
            map(lambda x: x.split("... | ...")),
            map(lambda x: filter(lambda y: y != "0", x)),
            map(lambda x: filter(lambda y: y != "", x)),
            map(lambda x: " | ".join(x)),
            list,
        )
        if not current_WM_value:
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        elif current_WM_value == second_dropdowns_obj["matched_items"][0]:
            # second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        elif current_WM_value != second_dropdowns_obj["matched_items"][0]:
            # second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
            sheet.set_cell_data(idx, 4, current_WM_value)
        elif current_WM_value not in second_dropdowns_obj["matched_items"]:
            # second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
            # sheet.set_cell_data(idx, 4, current_WM_value)
        else:
            pass

    for idx in all_row_index:
        update_row(idx)
        update_unitCell_inRow(idx)

    sheet.set_column_widths(state.wmCat_col_widths)
    sheet.set_all_row_heights(state.wmCat_row_heights)
    sheet.see(column=0)


def on_select_wmCatCombo(event, state):
    sheet = state.commonWM_sheet
    # print(dir(sheet))
    selected_kind = state.wmCat_comboBox.get()
    print(selected_kind)

    filtered_data = go(
        state.common_wm_data,
        filter(lambda x: selected_kind in str(x)),
        # map(lambda x: ["", x]),
        list,
    )
    sheet.set_sheet_data(filtered_data)
    sheet.set_column_widths(state.wmCat_col_widths)
    sheet.set_all_row_heights(state.wmCat_row_heights)
    sheet.see(column=0)


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
    sheet.header_font(("Arial", 9, "normal"))
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
