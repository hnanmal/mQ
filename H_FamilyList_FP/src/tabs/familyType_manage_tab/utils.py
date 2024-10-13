# src/tabs/familyType_manage_tab/utils.py
from itertools import chain
from copy import copy
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tksheet import Sheet
import os


def on_right_click_stdTypetree_roomTab(event, state, tree):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if item and column:
        menu = generate_context_menu_room(state, tree, item, column)
        menu.post(event.x_root, event.y_root)


def generate_context_menu_room(state, tree, item, column):
    menu = tk.Menu(tree, tearoff=0)
    actions = {
        "Edit": lambda: enable_tree_item_editing_room(state, tree, item, column),
        "Delete": lambda: del_stdType_roomCat(state),
        # Additional actions...
    }

    for label, command in actions.items():
        menu.add_command(label=label, command=command)

    return menu


def enable_tree_item_editing_room(state, tree, item, column):
    """Enable editing for the specified column of the treeview item."""
    x, y, width, height = tree.bbox(item, column)
    entry = tk.Entry(tree, width=width)

    oldType_name = tree.item(item, "values")[0]
    oldBd_tag = tree.item(item, "values")[1]

    def save_edit(event, column):
        new_value = entry.get()
        tree.set(item, column=column, value=new_value)
        entry.destroy()

        if column == "#1":
            for std_dic in state.project_info["std_types_roomCat"]:
                if (
                    std_dic["finish_type"] == oldType_name
                    and std_dic["building_tag"] == oldBd_tag
                ):
                    std_dic["finish_type"] = new_value

            ## 변한 키이름을 state.project_info["std_wm_assign"]에 연동
            state.project_info["std_wm_assign"][new_value] = state.project_info[
                "std_wm_assign"
            ].pop(oldType_name)

            ## 변한 키이름을 state.project_info["apply_target_rooms"]에 연동
            for room_dic in state.project_info["apply_target_rooms"]:
                if room_dic["stdType_tag"] == oldType_name:
                    room_dic["stdType_tag"] = new_value

        elif column == "#2":
            for std_dic in state.project_info["std_types_roomCat"]:
                if (
                    std_dic["finish_type"] == oldType_name
                    and std_dic["building_tag"] == oldBd_tag
                ):
                    std_dic["building_tag"] = new_value

            # ## 변한 키이름을 state.project_info["apply_target_rooms"]에 연동
            # for room_dic in state.project_info["apply_target_rooms"]:
            #     if room_dic["stdType_tag"] == oldType_name:
            #         room_dic["bd_tag"] = new_value

    # Get the current text in the cell
    current_value = tree.item(item, "values")[int(column[1:]) - 1]

    entry.insert(0, current_value)
    entry.place(x=x, y=y, width=width, height=height)

    entry.bind("<Return>", lambda e: save_edit(e, column))
    entry.bind("<FocusOut>", lambda event: entry.destroy())
    entry.focus()


def open_excel_locally(event):
    # excel_file_path = r"C:\Users\YourUsername\OneDrive\path_to_your_excel_file.xlsx"
    excel_file_path = r"https://henginmc6eaoutlook.sharepoint.com/:x:/s/WA00011298/EdjHwefslbpHrt_4sNEveBcBZ4V1Ov_22qasxDnTHyhVCg?e=puTs5C"
    os.startfile(excel_file_path)


def open_calcType_view(event, state):
    from src.tabs.calc_criteria_tab.calc_criteria_tab import create_calc_criteria_tab

    def select_item_by_value(treeview, column, value):
        # Iterate over all items in the treeview
        for child in treeview.get_children():
            # Get the value of the specified column for the current item
            item_value = treeview.item(child, "values")[column]
            print(item_value)
            # If the value matches, select the item
            print(item_value == value)
            if item_value == value:
                treeview.focus(child)
                treeview.selection_set(child)  ## 제대로 작동 안함. 확인 필요
                treeview.event_generate("<<TreeviewSelect>>")
                print(treeview.event_generate("<<TreeviewSelect>>"))
                treeview.see(child)  # Scroll to the selected item if needed
                break  # Exit after the first match is found

    window = tk.Toplevel()
    window.geometry("1280x800+100+100")
    window.wm_attributes("-topmost", 1)

    create_calc_criteria_tab(window, state, mode="newWindow_room")
    selected_calcType = state.selected_calcType_name.get().split(": ")[-1]
    select_item_by_value(
        state.calcType_treeview, column=0, value=selected_calcType.strip()
    )


def on_change_wmSheet(event, state, sheet):
    # update_second_cell_dropdown(event, state, sheet)

    selected_stdType_name = state.selected_stdType_name.get().split(": ")[-1]
    sheet_kind = sheet.headers()[0]
    print(sheet_kind)

    wmBunches = []
    for row in sheet.get_sheet_data():
        wm_row_dic = dict(zip(state.common_headers, row))
        wmBunches.append(wm_row_dic)

    # state.wmBunches_room = {}
    if state.project_info["std_wm_assign"][selected_stdType_name]:
        state.project_info["std_wm_assign"][selected_stdType_name][
            sheet_kind
        ] = wmBunches
    else:
        state.wmBunches_room.update({sheet_kind: wmBunches})

        # state.project_info["std_wm_assign"] = {}
        state.project_info["std_wm_assign"].update(
            {selected_stdType_name: state.wmBunches_room}
        )

    state.logging_text_widget.write(("\n").join(list(map(str, wmBunches))))


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


def add_room_to_apply_target_rooms(event, state, sheet):
    all_row_index = list(range(sheet.get_total_rows()))

    def chk_isExist(sheet, idx):
        sheet_room_no = sheet.get_cell_data(idx, 0)
        sheet_room_name = sheet.get_cell_data(idx, 1)
        if sheet_room_no != "" and sheet_room_name != "":
            chk_basket = list(
                map(
                    lambda x: x["room_no"] + x["room_name"],
                    state.project_info["apply_target_rooms"],
                )
            )
            if sheet_room_no + sheet_room_name not in chk_basket:
                return True, sheet_room_no, sheet_room_name
            else:
                return [False]
        else:
            return [False]

    for idx in all_row_index:
        if chk_isExist(sheet, idx)[0]:
            state.project_info["apply_target_rooms"].append(
                {
                    "room_name": chk_isExist(sheet, idx)[2],
                    "room_no": chk_isExist(sheet, idx)[1],
                    "finish_type": "",
                    "stdType_tag": "",
                    "bd_tag": "",
                    "calc_tag": "",
                }
            )


# Function to update the second cell dropdown (B1) based on the first cell selection
def update_second_cell_dropdown(event, state, sheet):
    all_row_index = list(range(sheet.get_total_rows()))
    print(all_row_index)

    # print(second_dropdowns)
    # Set the second cell's dropdown based on the first cell's value
    def update_unitCell_inRow(idx):
        if sheet.get_cell_data(idx, 4):
            selected_value = sheet.get_cell_data(idx, 4)
            unit_info = selected_value.split("... | ...")[-4]
            sheet.set_cell_data(idx, 2, unit_info)

    def update_row(idx):
        selected_value = sheet.get_cell_data(idx, 0)
        # print(selected_value)
        try:
            current_WM_value = copy(
                sheet.get_cell_data(idx, 4)
            )  # Get selected value from the first cell
        except:
            current_WM_value = None
        print(current_WM_value)
        second_dropdowns_obj = state.wm_group_data.get(
            selected_value, {"matched_items": []}
        )
        # map(lambda x: x.split("... | ..."), second_dropdowns_obj["matched_items"])
        print(current_WM_value == second_dropdowns_obj["matched_items"][0])
        if not current_WM_value:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        elif current_WM_value == second_dropdowns_obj["matched_items"][0]:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
        elif current_WM_value != second_dropdowns_obj["matched_items"][0]:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
            sheet.set_cell_data(idx, 4, current_WM_value)
        elif current_WM_value not in second_dropdowns_obj["matched_items"]:
            second_dropdowns = second_dropdowns_obj["matched_items"]
            sheet.create_dropdown(idx, 4, values=second_dropdowns)
            # sheet.set_cell_data(idx, 4, current_WM_value)
        else:
            pass

    for idx in all_row_index:
        update_row(idx)
        update_unitCell_inRow(idx)


# from src.tabs.input_common_tab.utils import create_defaultTreeview
def create_assignWMsheet(
    state, frame, headers=[], height=None, width=None, dropdowns=None
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
    )

    # sheet_data = [["", ""], ["", ""], ["", ""]]

    sheet.header_font(("Arial", 9, "normal"))
    sheet.set_options(font=("Arial Narrow", 8, "normal"))  # Font name and size
    sheet.set_sheet_data()

    sheet.set_column_widths(state.common_widths)

    # Bind event to detect changes in the first cell (A1) and update the second cell
    sheet.extra_bindings(
        [
            (
                "rc_insert_row",
                lambda e: add_assignRow(e, state, sheet, dropdowns),
            ),
            (
                "end_edit_cell",
                # lambda e: update_second_cell_dropdown(e, state, sheet),
                lambda e: on_change_wmSheet(e, state, sheet),
            ),
            (
                "cell_select",
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
    selected_calcType_sheetview,
):
    if calc_comboBox.get():
        selected_calcType = calc_comboBox.get()
        state.selected_calcType_name.set("Selected Calc Type: " + selected_calcType)

    else:
        selected_calcType = state.selected_calcType_name.get().split(": ")[-1]
        # print(selected_calcType)
    selectedCalcDic = list(
        filter(
            lambda x: x["type_tag"] == selected_calcType,
            state.project_info["calc_types"],
        )
    )[0]
    selectedCalc_model_params = selectedCalcDic["model_params"]
    selectedCalc_manual_params = selectedCalcDic["manual_params"]
    selectedCalc_params = selectedCalc_model_params + selectedCalc_manual_params
    selected_calcType_sheetview.set_sheet_data([])
    paramDatas = []
    for param_dic in selectedCalc_params:
        c1 = param_dic["항목"]
        c2 = param_dic["수식 약자"]
        c3 = param_dic.get("수동입력값", "byRevit")
        paramDatas.append([c1, c2, c3])
    selected_calcType_sheetview.set_sheet_data(paramDatas)


def update_selected_stdType_label_inRoom(
    event, state, stdTypes_treeview, selected_stdType_label
):
    if stdTypes_treeview.focus():
        selected_type = stdTypes_treeview.item(stdTypes_treeview.focus())
        selected_type_name = selected_type.get("values")[0]

        state.selected_stdType_name.set("Selected Standard Type: " + selected_type_name)
    else:
        state.selected_stdType_name.set("Selected Standard Type: ")

    # return selected_type_name


def add_stdType_roomCat(state, new_stdType_text):
    stdType_input = new_stdType_text.get("1.0", tk.END).strip()
    if stdType_input:
        stdTypes = stdType_input.split("\n")
        for stdType in stdTypes:
            if stdType.strip():
                stdType_name = stdType.strip()
                state.project_info["std_types_roomCat"].append(
                    {
                        "finish_type": stdType_name,
                        "building_tag": "",
                    }
                )
                state.stdTypeTree_inRoom.insert("", "end", values=(stdType_name, ""))
                state.logging_text_widget.write(
                    f"add [ {stdType_name} ] Standard Type.\n"
                )
        new_stdType_text.delete("1.0", tk.END)


def del_stdType_roomCat(state):
    selected_stdTypes = state.stdTypeTree_inRoom.selection()
    selected_building = state.selected_building
    for selected_stdType in selected_stdTypes:
        selected_stdType_name = state.stdTypeTree_inRoom.item(
            selected_stdType, "values"
        )[0]
        state.logging_text_widget.write(
            f"remove [ {selected_stdType_name} ] Standard Type.\n"
        )
        for room_dic in state.project_info["apply_target_rooms"]:
            if (
                room_dic["stdType_tag"] == selected_stdType_name
                and room_dic["bd_tag"] == selected_building
            ):
                room_dic["stdType_tag"] = ""
                room_dic["bd_tag"] = ""
                room_dic["calc_tag"] = ""

        for stdType_dic in state.project_info["std_types_roomCat"]:
            if stdType_dic["finish_type"] == selected_stdType_name:
                state.project_info["std_types_roomCat"].remove(stdType_dic)

        state.stdTypeTree_inRoom.delete(selected_stdType)


def update_stdTypeTree_inRoom(event, state, bd_comboBox):

    update_selected_calcType(
        event,
        state,
        state.calc_comboBox_room,
        state.selected_calcType_label,
        state.selected_calcType_sheetview,
    )

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

    if not state.project_info.get("std_types_roomCat"):
        find_all_stdType_items_inRoom()

    state.stdTypeTree_inRoom.delete(*state.stdTypeTree_inRoom.get_children())

    stdType_items_inRoom = state.project_info["std_types_roomCat"]

    for dic in stdType_items_inRoom:
        print(dic)
        state.stdTypeTree_inRoom.insert("", "end", values=list(dic.values()))


def update_combobox_data(combobox, data, mode=None, cat=None):
    """
    Update the combobox values based on the data loaded from the JSON file.
    """
    if mode == "building":
        items = data.get("building_list", [])
        building_names = list(map(lambda x: x["building_name"], items))

        # Update the combobox values
        combobox["values"] = ["프로젝트 공통"] + building_names

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


def update_notAppliedRoom_data(state):
    # print(state.project_info.get("apply_target_rooms"))
    if not state.project_info.get("apply_target_rooms"):
        not_applied_rooms = []
        for bd_dic in state.project_info["building_list"]:
            bd_tag = bd_dic["building_name"]
            room_list = bd_dic["room_list"]
            for room_dic in room_list:
                room_dic["stdType_tag"] = ""
                room_dic["bd_tag"] = bd_tag
                room_dic["calc_tag"] = ""
                not_applied_rooms.append(room_dic)
        state.project_info["apply_target_rooms"] = not_applied_rooms
        # print(not_applied_rooms)
    # elif "apply_target_rooms" in state.project_info:
    #     pass


def on_click_stdTypeLabel(event, state, stdTypes_treeview, selected_stdType_label):
    WMsheets = [
        state.assignWM_sheetview_forStdType_forFloor,
        state.assignWM_sheetview_forStdType_forBase,
        state.assignWM_sheetview_forStdType_forWall,
        state.assignWM_sheetview_forStdType_forCeiling,
    ]

    def init_WMsheetviews(state, sheet):
        sheet.set_sheet_data([])
        sheet.set_column_widths(state.common_widths)

    for wmsheet in WMsheets:
        init_WMsheetviews(state, wmsheet)
    selected_building = state.bd_combobox_room.get()
    state.selected_building = selected_building
    current_selected_stdType = stdTypes_treeview.item(stdTypes_treeview.focus())
    selected_type_name = current_selected_stdType.get("values")[0]

    update_selected_stdType_label_inRoom(
        event, state, stdTypes_treeview, selected_stdType_label
    )

    ##### assignWM_sheetview 영역 업데이트 구간
    def set_first_cell_forSheet(sheet, data, dropdowns):
        # sheet.set_sheet_data([])
        sheet.update_idletasks()
        sheet.set_sheet_data(data)
        sheet.set_column_widths(state.common_widths)
        for idx in list(range(len(data))):
            firstCell = data[idx][0]
            sheet.create_dropdown(idx, 0, values=state.floor_dropdowns)
            sheet.set_cell_data(
                idx,
                0,
                firstCell,
            )

    if not state.project_info["std_wm_assign"].get(selected_type_name):
        state.project_info["std_wm_assign"][selected_type_name] = {
            "Floor": [],
            "Base": [],
            "Wall": [],
            "Ceiling": [],
        }
    else:
        pass

    data = state.project_info["std_wm_assign"][selected_type_name]
    floor_data = list(map(lambda x: list(x.values()), data["Floor"]))
    base_data = list(map(lambda x: list(x.values()), data["Base"]))
    wall_data = list(map(lambda x: list(x.values()), data["Wall"]))
    ceiling_data = list(map(lambda x: list(x.values()), data["Ceiling"]))

    set_first_cell_forSheet(
        state.assignWM_sheetview_forStdType_forFloor,
        floor_data,
        state.floor_dropdowns,
    )
    set_first_cell_forSheet(
        state.assignWM_sheetview_forStdType_forBase,
        base_data,
        state.base_dropdowns,
    )
    set_first_cell_forSheet(
        state.assignWM_sheetview_forStdType_forWall,
        wall_data,
        state.wall_dropdowns,
    )
    set_first_cell_forSheet(
        state.assignWM_sheetview_forStdType_forCeiling,
        ceiling_data,
        state.ceil_dropdowns,
    )

    ##### combobox update ######
    state.calc_comboBox_room.update_idletasks()

    ##### Applied / notApplied_famType_sheetview 우측 영역 업데이트 구간

    if state.selected_calcType_name.get() != "Selected Calc Type: ":
        items = state.project_info.get("calc_types", [])
        calcType_names = list(
            map(
                lambda x: x["type_tag"],
                filter(lambda x: x["category"] == "Room", items),
            )
        )
        state.selected_calcType_name.set("Selected Calc Type: " + calcType_names[0])

    print("!!!" + selected_building)

    applied_famType_sheetview = state.applied_famType_sheetview
    notApplied_famType_sheetview = state.notApplied_famType_sheetview
    notApplied_famType_sheetview.set_sheet_data([])

    apply_target_rooms = state.project_info["apply_target_rooms"]

    applied_famType_sheetview.clear()
    notApplied_famType_sheetview.clear()
    idxs = range(len(apply_target_rooms))
    applies = []
    not_applies = []
    for rowidx in idxs:
        if (
            apply_target_rooms[rowidx]["bd_tag"] == selected_building
            and apply_target_rooms[rowidx]["stdType_tag"] == selected_type_name
        ):
            # apply_target_rooms[rowidx][
            #     "calc_tag"
            # ] = state.selected_calcType_name.get().split(": ")[-1]
            applies.append(
                [
                    apply_target_rooms[rowidx]["room_no"],
                    apply_target_rooms[rowidx]["room_name"],
                    apply_target_rooms[rowidx]["stdType_tag"],
                    apply_target_rooms[rowidx]["bd_tag"],
                    apply_target_rooms[rowidx]["calc_tag"],
                ]
            )
        elif apply_target_rooms[rowidx]["calc_tag"] == "":
            not_applies.append(
                [
                    apply_target_rooms[rowidx]["room_no"],
                    apply_target_rooms[rowidx]["room_name"],
                    apply_target_rooms[rowidx]["stdType_tag"],
                    apply_target_rooms[rowidx]["bd_tag"],
                ]
            )

    applied_famType_sheetview.set_sheet_data(applies)
    notApplied_famType_sheetview.set_sheet_data(not_applies)

    applied_famType_sheetview.column_width(0, 30)
    applied_famType_sheetview.column_width(1, 170)
    notApplied_famType_sheetview.column_width(0, 30)
    notApplied_famType_sheetview.column_width(1, 170)


def add_to_appliedRoom_data(state):
    # selected_items = state.notApplied_famType_sheetview.get_currently_selected()
    selected_items = list(state.notApplied_famType_sheetview.get_selected_cells())
    print(selected_items)

    def add_oneRow(selected_item):
        # selectedRow = selected_item.row
        selectedRow = selected_item[0]
        roomNo = state.notApplied_famType_sheetview.get_cell_data(selectedRow, 0)
        roomName = state.notApplied_famType_sheetview.get_cell_data(selectedRow, 1)

        for room_dic in state.project_info["apply_target_rooms"]:
            if room_dic["room_no"] == roomNo and room_dic["room_name"] == roomName:
                room_dic["stdType_tag"] = state.selected_stdType_name.get().split(": ")[
                    -1
                ]
                room_dic["bd_tag"] = state.selected_building
                room_dic["calc_tag"] = state.selected_calcType_name.get().split(": ")[
                    -1
                ]

                state.logging_text_widget.write(str(room_dic))

        appliedRooms = state.applied_famType_sheetview.get_sheet_data()
        for room_dic in state.project_info["apply_target_rooms"]:
            if room_dic["room_no"] == roomNo and room_dic["room_name"] == roomName:
                appliedRooms.append(
                    [
                        room_dic["room_no"],
                        room_dic["room_name"],
                        room_dic["stdType_tag"],
                        room_dic["bd_tag"],
                        room_dic["calc_tag"],
                    ]
                )
        state.applied_famType_sheetview.set_sheet_data(appliedRooms)

    if state.bd_combobox_room.get() == "대상 빌딩 선택":
        state.logging_text_widget.write("!!! 화면 상단에서 빌딩을 선택해 주세요 !!!")
    else:
        for selected_item in selected_items:
            add_oneRow(selected_item)
        for selected_item in list(reversed(selected_items)):
            state.notApplied_famType_sheetview.delete_row(selected_item[0])

    state.applied_famType_sheetview.column_width(0, 30)
    state.applied_famType_sheetview.column_width(1, 170)
    state.notApplied_famType_sheetview.column_width(0, 30)
    state.notApplied_famType_sheetview.column_width(1, 170)


def remove_from_appliedRoom_data(state):
    # selected_item = state.applied_famType_sheetview.get_currently_selected()
    selected_items = list(state.applied_famType_sheetview.get_selected_cells())

    def remove_oneRow(selected_item):
        # selectedRow = selected_item.row
        selectedRow = selected_item[0]
        roomNo = state.applied_famType_sheetview.get_cell_data(selectedRow, 0)
        roomName = state.applied_famType_sheetview.get_cell_data(selectedRow, 1)

        for room_dic in state.project_info["apply_target_rooms"]:
            if room_dic["room_no"] == roomNo and room_dic["room_name"] == roomName:
                room_dic["stdType_tag"] = ""
                room_dic["bd_tag"] = ""
                room_dic["calc_tag"] = ""

                state.logging_text_widget.write(str(room_dic))

        notAppliedRooms = []
        for room_dic in state.project_info["apply_target_rooms"]:
            if room_dic["bd_tag"] == "":
                notAppliedRooms.append(
                    [
                        room_dic["room_no"],
                        room_dic["room_name"],
                        room_dic["stdType_tag"],
                        room_dic["bd_tag"],
                    ]
                )
        # print(notAppliedRooms)
        state.notApplied_famType_sheetview.set_sheet_data(notAppliedRooms)
        # state.applied_famType_sheetview.delete_row(selectedRow)

    for selected_item in selected_items:
        remove_oneRow(selected_item)
    # for selected_item in list(reversed(selected_items)):
    for selected_item in selected_items:
        state.applied_famType_sheetview.delete_row(selected_item[0])

    state.applied_famType_sheetview.column_width(0, 30)
    state.applied_famType_sheetview.column_width(1, 170)
    state.notApplied_famType_sheetview.column_width(0, 30)
    state.notApplied_famType_sheetview.column_width(1, 170)


def save_project_roomType_info(state):
    from src.tabs.project_info_tab.common_utils import load_project_info

    project_info_ = state.project_info

    file_path = filedialog.asksaveasfilename(
        defaultextension=".hpjt",  # Default file extension
        filetypes=[("HPJT files", "*.hpjt"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")

    load_project_info(
        state,
        state.project_name_var,
        state.project_type_var,
        state.building_treeview,
        state.earth_treeview,
        state.steel_treeview,
        file_path_arg=file_path,
    )
