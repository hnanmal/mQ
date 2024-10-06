# src/tabs/familyType_manage_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tksheet import Sheet


def add_assignRow(event, state, sheet, dropdowns=None):
    new_row_index = sheet.get_total_rows()  # Get the current total rows
    if state.stdTypeTree_inRoom.selection():
        sheet.insert_rows(idx=new_row_index)
        if dropdowns:
            sheet.create_dropdown(new_row_index, 0, values=dropdowns)
            sheet.set_cell_data(new_row_index, 0, "")
    else:
        new_row_index = sheet.get_total_rows()
        state.logging_text_widget.write(
            ":: !!!스탠다드 타입을 선택하셔야 동작합니다!!! ::"
        )
    sheet.del_row(new_row_index - 1)


def dropdown_selected(event, sheet):
    sheet.set_column_widths(
        [120, 100, 70, 30, 800, 100, 100, 100],
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
        # map(lambda x: x.split("... | ..."), second_dropdowns_obj["matched_items"])
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

    sheet.header_font(("Arial", 9, "normal"))
    sheet.set_options(font=("Arial Narrow", 8, "normal"))  # Font name and size
    sheet.set_sheet_data()

    sheet.set_column_widths(
        [120, 100, 70, 30, 800, 100, 100, 100],
    )

    # Bind event to detect changes in the first cell (A1) and update the second cell
    sheet.extra_bindings(
        [
            (
                "rc_insert_row",
                lambda e: add_assignRow(e, state, sheet, dropdowns),
            ),
            (
                # "end_edit_cell",
                "edit_cell",
                lambda e: update_second_cell_dropdown(e, state, sheet),
            ),
        ]
    )

    return sheet


def create_tksheet(
    state, frame, headers=[], data=[], height=None, width=None, mode=None
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

    sheet.header_font(("Arial", 9, "normal"))
    sheet.set_options(font=("Arial Narrow", 8, "normal"))  # Font name and size
    sheet.set_sheet_data()
    if mode == "nonAppFamtype":
        sheet.column_width(0, 300)
    elif mode == "calcType":
        sheet.column_width(1, 50)

    # sheet.set_column_widths(
    #     [120, 100, 70, 70, 800, 100, 100, 100],
    # )

    return sheet


def update_selected_calcType(
    event,
    state,
    calc_comboBox,
    selected_calcType_label,
    selected_calcType_treeview,
):
    if calc_comboBox.get():
        selected_type = calc_comboBox.get()
        state.selected_calcType_name.set("Selected Calc Type: " + selected_type)

        selectedCalcDic = list(
            filter(
                lambda x: x["type_tag"] == selected_type,
                state.project_info["calc_types"],
            )
        )[0]
        selectedCalc_model_params = selectedCalcDic["model_params"]
        selectedCalc_manual_params = selectedCalcDic["manual_params"]
        selectedCalc_params = selectedCalc_model_params + selectedCalc_manual_params
        for param_dic in selectedCalc_params:
            c1 = param_dic["항목"]
            c2 = param_dic["수식 약자"]
            c3 = param_dic.get("수동입력값", "byRevit")
            selected_calcType_treeview.insert("", "end", values=[c1, c2, c3])
    else:
        state.selected_calcType_name.set("Selected Calc Type:          ")


def update_selected_stdType_label_inRoom(
    event, state, stdTypes_treeview, selected_stdType_label
):
    if stdTypes_treeview.focus():
        selected_type = stdTypes_treeview.item(stdTypes_treeview.focus())
        selected_type_name = selected_type.get("values")[0]

        state.selected_stdType_name.set("Selected Standard Type: " + selected_type_name)
    else:
        state.selected_stdType_name.set("Selected Standard Type: ")


def update_stdTypeTree_inRoom(event, state, bd_comboBox):
    def find_unique_dic(dics):
        criteria = []
        res = []
        for dic in dics:
            if str(dic) not in criteria:
                criteria.append(str(dic))
                res.append(dic)
        return res

    def find_all_stdType_items_inRoom():  ## 여기 말고 로드 함수로 옮겨서 로드하자마자 state 에 일단 stdTypeDic 초안을 업데이트 하게 해야 하지 않나?
        res = []
        for bd_dic in state.project_info["building_list"]:
            for room_dic in bd_dic["room_list"]:
                res.append(
                    {
                        "finish_type": room_dic["finish_type"],
                        "building_tag": bd_dic["building_name"],
                    }
                )
                # res.append(room_dic["finish_type"])
        all_stdType_items_inRoom = res
        state.project_info["std_types_roomCat"] = find_unique_dic(
            all_stdType_items_inRoom
        )
        # print(all_stdType_items_inRoom)
        return res

    find_all_stdType_items_inRoom()

    def find_stdType_items_inRoom_atBD(selectedBuilding):
        res = []
        if selectedBuilding:
            for stdType_dic in state.project_info["std_types_roomCat"]:
                if stdType_dic["building_tag"] == selectedBuilding:
                    # res.append(stdType_dic["finish_type"])
                    res.append(stdType_dic)
        return res

    state.stdTypeTree_inRoom.delete(*state.stdTypeTree_inRoom.get_children())

    print(state.project_info["std_types_roomCat"])

    # stdType_items_inRoom = list(set(find_stdType_items_inRoom_atBD(bd_comboBox.get())))
    # stdType_items_inRoom = find_stdType_items_inRoom_atBD(bd_comboBox.get())
    stdType_items_inRoom = state.project_info["std_types_roomCat"]
    for dic in stdType_items_inRoom:
        print(dic)
        # state.stdTypeTree_inRoom.insert("", "end", text=dic, values=[dic.items()])
        state.stdTypeTree_inRoom.insert("", "end", values=list(dic.values()))

    ##### notApplied_famType_sheetview 업데이트 구간
    current_selected_building = state.bd_combobox_room.get()
    print("!!!" + current_selected_building)
    notApplied_famType_sheetview = state.notApplied_famType_sheetview
    notApplied_famType_sheetview.set_sheet_data([])
    data = list(
        filter(
            lambda x: x["building_name"] == current_selected_building,
            state.project_info["building_list"],
        )
    )[0]["room_list"]
    # print(data)

    idxs = range(len(data))
    for rowidx in idxs:
        notApplied_famType_sheetview.insert_rows()
        notApplied_famType_sheetview.set_cell_data(
            rowidx,
            0,
            data[rowidx]["room_no"] + "_" + data[rowidx]["room_name"],
        )
    notApplied_famType_sheetview.column_width(0, 300)


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
