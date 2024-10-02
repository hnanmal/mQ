# src/tabs/familyType_manage_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tksheet import Sheet


def add_assignRow(event, state, sheet, dropdowns=None):
    new_row_index = sheet.get_total_rows()  # Get the current total rows
    sheet.insert_rows(idx=new_row_index)
    if dropdowns:
        sheet.create_dropdown(new_row_index, 0, values=dropdowns)
    sheet.del_row(new_row_index - 1)


def dropdown_selected(event, sheet):
    sheet.set_column_widths(
        [120, 100, 70, 70, 800, 100, 100, 100],
    )  # Sets the first column's width to 150 pixels
    print("!!!")


# Function to update the second cell dropdown (B1) based on the first cell selection
def update_second_cell_dropdown(event, state, sheet):
    all_row_index = list(range(sheet.get_total_rows()))
    print(all_row_index)
    # print(second_dropdowns)
    # Set the second cell's dropdown based on the first cell's value

    def update_row(idx):
        selected_value = sheet.get_cell_data(idx, 0)
        print(selected_value)
        try:
            current_WM_value = sheet.get_cell_data(
                idx, 4
            )  # Get selected value from the first cell
        except:
            current_WM_value = None
        second_dropdowns_obj = state.wm_group_data.get(selected_value)

        if not current_WM_value:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        elif current_WM_value == second_dropdowns_obj["matched_items"][0]:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        elif current_WM_value not in second_dropdowns_obj["matched_items"]:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        else:
            pass

    for idx in all_row_index:
        update_row(idx)
        # sheet.horizontal_scrollbar.set(0, 0)  # Reset the scrollbar to the far left
        # state.update_idletasks()  # Ensure GUI updates

    # sheet.set_column_widths(
    #     [120, 100, 100, 800, 100, 100, 100],
    # )
    print("!!!")
    # Optionally clear the value of the second cell when updating the dropdown
    # sheet.set_cell_data(0, 1, "")


# from src.tabs.input_common_tab.utils import create_defaultTreeview
def create_assignWMsheet(
    state, frame, headers=[], height=None, width=None, dropdowns=None
):
    sheet = Sheet(frame, headers=headers, height=height, width=width)
    sheet.enable_bindings(
        "edit_cell",
        "single_select",  # Allow single cell selection
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
    )

    # sheet_data = [["", ""], ["", ""], ["", ""]]

    sheet.set_options(font=("Arial Narrow", 9, "normal"))  # Font name and size
    sheet.set_sheet_data()
    # if dropdowns:
    #     sheet.create_dropdown(0, 0, values=dropdowns)

    sheet.set_column_widths(
        [120, 100, 70, 70, 800, 100, 100, 100],
    )

    # Bind event to detect changes in the first cell (A1) and update the second cell
    sheet.extra_bindings(
        [
            (
                "rc_insert_row",
                lambda e: add_assignRow(e, state, sheet, dropdowns),
            ),
            (
                "end_edit_cell",
                lambda e: update_second_cell_dropdown(e, state, sheet),
            ),
        ]
    )

    return sheet


def update_selected_stdType_label_inRoom(
    event, state, stdTypes_treeview, selected_stdType_label
):
    selected_type = stdTypes_treeview.item(stdTypes_treeview.focus())
    selected_type_name = selected_type.get("values")[0]

    state.selected_stdType_name.set("Selected Standard Type: " + selected_type_name)


def update_stdTypeTree_inRoom(event, state, bd_comboBox):
    def find_stdType_items_inRoom(selectedBuilding=None):
        res = []
        if selectedBuilding:
            for bd_dic in state.project_info["building_list"]:
                if bd_dic["building_name"] == selectedBuilding:
                    for room_dic in bd_dic["room_list"]:
                        res.append(room_dic["finish_type"])
        else:
            for bd_dic in state.project_info["building_list"]:
                for room_dic in bd_dic["room_list"]:
                    res.append(room_dic["finish_type"])
        return res

    state.stdTypeTree_inRoom.delete(*state.stdTypeTree_inRoom.get_children())

    stdType_items_inRoom = list(set(find_stdType_items_inRoom(bd_comboBox.get())))
    for i in stdType_items_inRoom:
        print(i)
        state.stdTypeTree_inRoom.insert("", "end", text=i, values=[i])


def search_stdTypes():
    pass


def create_stdTypes_listbox():
    pass


def update_combobox_data(combobox, data, mode=None, cat=None):
    """
    Update the combobox values based on the data loaded from the JSON file.
    """
    if mode == "building":
        items = data.get("building_list", [])
        building_names = list(map(lambda x: x["building_name"], items))

        # Update the combobox values
        combobox["values"] = building_names

        # Set the default value to the first item if available
        if building_names:
            combobox.set("대상 빌딩 선택")
        else:
            combobox.set("")  # Clear the combobox if no items are available
    elif mode == "calc":
        items = data.get("calc_types", [])
        calcType_names = list(
            map(lambda x: x["type_tag"], filter(lambda x: x["category"] == cat, items))
        )

        # Update the combobox values
        combobox["values"] = calcType_names

        # Set the default value to the first item if available
        if calcType_names:
            combobox.set(calcType_names[0])
        else:
            combobox.set("")  # Clear the combobox if no items are available


def save_project_roomType_info(state):
    project_info_ = state.project_info

    file_path = filedialog.asksaveasfilename(
        defaultextension=".hpjt",  # Default file extension
        filetypes=[("HPJT files", "*.hpjt"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")
