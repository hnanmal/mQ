import tkinter as tk
from tksheet import Sheet


def create_tksheet(
    state, frame, headers=[], data=[], tab_name=None, height=None, width=None, mode=None
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

    sheet.set_sheet_data(data)
    sheet.kind = None
    # sheet.set_column_widths(state[tab_name]["common_widths"])

    # sheet.extra_bindings(
    #     [
    #         (
    #             "rc_insert_row",
    #             lambda e: add_assignRow_allCat(e, state, sheet, tab_name=tab_name),
    #         ),
    #         (
    #             "rc_delete_row",
    #             lambda e: on_change_wmSheet_allCat(
    #                 e, state, sheet, tab_name, mode="stdType"
    #             ),
    #         ),
    #         (
    #             "end_edit_cell",
    #             # lambda e: update_second_cell_dropdown(e, state, sheet),
    #             lambda e: on_change_wmSheet_allCat(
    #                 e, state, sheet, tab_name, mode="stdType"
    #             ),
    #         ),
    #         (
    #             "cell_select",
    #             lambda e: update_second_cell_dropdown_allCat(e, state, sheet, tab_name),
    #         ),
    #     ]
    # )

    return sheet


def convert_GWMsheet_data_to_dict(sheet_data):
    sheet_data_dict = {}
    current_parent = None
    current_sub_parent = None

    for row in sheet_data:
        if row[0]:  # Top-level parent
            current_parent = row[0]
            sheet_data_dict[current_parent] = {}
        elif row[1]:  # Sub-level parent
            current_sub_parent = row[1]
            sheet_data_dict[current_parent][current_sub_parent] = []
        elif row[2]:  # Children
            sheet_data_dict[current_parent][current_sub_parent].append(row[2])

    return sheet_data_dict


def parse_sheet_toJson(sheet, mode=None):
    _sheet_data = sheet.get_sheet_data()
    if not mode:
        mode = sheet.kind

    if mode == "GWM":
        sheet_data = convert_GWMsheet_data_to_dict(_sheet_data)

    return sheet_data


def populate_tksheet(state, sheet):
    pass
