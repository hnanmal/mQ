import tkinter as tk
from tkinter import ttk
from tksheet import Sheet


def create_tksheet_commonWM(
    state, frame, headers=[], data=[], tab_name=None, height=None, width=None, mode=None
):

    sheet = Sheet(frame, headers=headers, height=height, width=width)
    sheet.enable_bindings(
        "edit_cell",
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
        "rc_insert_row",
        "rc_delete_row",
        "arrowkeys",
    )
    sheet.header_font(("Arial", 9, "normal"))
    sheet.set_options(font=("Arial Narrow", 8, "normal"))  # Font name and size

    sheet.set_sheet_data()
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
    #             lambda e: update_second_cell_dropdown_allCat(e, state, sheet),
    #         ),
    #     ]
    # )

    return sheet
