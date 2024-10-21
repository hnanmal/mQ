from src.tabs.familyType_manage_tab.utils import update_selected_calcType
import tkinter as tk
from tksheet import Sheet
from copy import copy
from copy import deepcopy


def add_stdType_allCat(state, new_stdType_text, tab_name):
    stdType_input = new_stdType_text.get("1.0", tk.END).strip()
    if stdType_input:
        stdTypes = stdType_input.split("\n")
        for stdType in stdTypes:
            if stdType.strip():
                stdType_name = stdType.strip()
                state.project_info["std_types"][tab_name].append(
                    {
                        "std_type": stdType_name,
                        "building_tag": "",
                        "cat_tag": tab_name,
                        "wmGrps": [],
                    }
                )
                state[tab_name]["stdTypeTree"].insert(
                    "", "end", values=(stdType_name, "")
                )
                state.logging_text_widget.write(
                    f"add [ {stdType_name} ] Standard Type.\n"
                )
        new_stdType_text.delete("1.0", tk.END)


def del_stdType_allCat(state, tab_name):
    selected_stdTypes = state[tab_name]["stdTypeTree"].selection()
    selected_building = state.selected_building
    for selected_stdType in selected_stdTypes:
        selected_stdType_name = state[tab_name]["stdTypeTree"].item(
            selected_stdType, "values"
        )[0]
        state.logging_text_widget.write(
            f"remove [ {selected_stdType_name} ] Standard Type.\n"
        )

        # 룸 이외 카테고리용으로 수정 필요
        for idx, rvtType_dic in enumerate(
            state.project_info["apply_target_rvtTypes"][tab_name]
        ):
            if (
                rvtType_dic["stdType_tag"] == selected_stdType_name
                and rvtType_dic["bd_tag"] == selected_building
            ):
                del state.project_info["apply_target_rvtTypes"][tab_name][idx]
                # rvtType_dic["stdType_tag"] = ""
                # rvtType_dic["bd_tag"] = ""
                # rvtType_dic["calc_tag"] = ""

        for stdType_dic in state.project_info["std_types"][tab_name]:
            if stdType_dic["std_type"] == selected_stdType_name:
                state.project_info["std_types"][tab_name].remove(stdType_dic)

        state[tab_name]["stdTypeTree"].delete(selected_stdType)


def update_selected_stdType_label_allCat(
    event,
    state,
    stdTypes_treeview,
    tab_name=None,
):
    if stdTypes_treeview.focus():
        selected_type = stdTypes_treeview.item(stdTypes_treeview.focus())
        state[tab_name]["selected_stdType"] = selected_type
        selected_type_name = selected_type.get("values")[0]

        state[tab_name]["selected_stdType_name"].set(
            "Selected Standard Type: " + selected_type_name
        )
    else:
        state[tab_name]["selected_stdType_name"].set("Selected Standard Type: ")


def on_click_stdType_treeItem_allCat(
    event,
    state,
    stdTypes_treeview,
    sheet_input=None,
    tab_name=None,
):
    if sheet_input:
        WMsheet = sheet_input
    else:
        WMsheet = state[tab_name]["assignWM_sheetview_forStdType"]

    def init_WMsheetviews(state, sheet, selected_type_name):
        wmGrps = list(
            map(
                lambda x: x["wmGrps"],
                filter(
                    lambda x: x["std_type"] == selected_type_name,
                    state.project_info["std_types"][tab_name],
                ),
            )
        )[0]
        wmGrps_tr = []
        for i in wmGrps:
            wmGrps_tr.append([i, ""])

        hdrs = sheet.headers()
        sheet.reset()
        # sheet.set_sheet_data(wmGrps)
        sheet.set_sheet_data(wmGrps_tr)
        sheet.set_column_widths(state[tab_name]["common_widths"])
        sheet.set_header_data(hdrs)

    selected_building = state.selected_building
    current_selected_stdType = stdTypes_treeview.item(stdTypes_treeview.focus())
    state[tab_name]["selected_stdType"] = current_selected_stdType

    if current_selected_stdType.get("values"):
        selected_type_name = current_selected_stdType.get("values")[0]
        if state.project_info["std_wm_assign_allCat"][tab_name].get(selected_type_name):
            WMsheet.set_column_widths(state[tab_name]["common_widths"])
            pass
        else:
            init_WMsheetviews(state, WMsheet, selected_type_name)

    update_selected_stdType_label_allCat(
        event, state, stdTypes_treeview, tab_name=tab_name
    )

    ##### assignWM_sheetview 영역 업데이트 구간
    def set_data_forSheet(sheet, data):
        # sheet.set_sheet_data([])
        sheet.update_idletasks()
        sheet.set_sheet_data(data)
        sheet.set_column_widths(state[tab_name]["common_widths"])
        # for idx in list(range(len(data))):
        #     firstCell = data[idx][0]
        #     sheet.create_dropdown(idx, 0, values=state.floor_dropdowns)
        #     sheet.set_cell_data(
        #         idx,
        #         0,
        #         firstCell,
        #     )

    if not state.project_info.get("std_wm_assign_allCat"):
        state.project_info["std_wm_assign_allCat"] = {}
        state.project_info["std_wm_assign_allCat"][tab_name] = {}

    if state.project_info["std_wm_assign_allCat"][tab_name].get(selected_type_name):
        data_dic = state.project_info["std_wm_assign_allCat"][tab_name][
            selected_type_name
        ]
        data = list(map(lambda x: list(x.values()), data_dic))
        print(data)
        set_data_forSheet(
            state[tab_name]["assignWM_sheetview_forStdType"],
            data,
        )
    ##### combobox update ######
    state[tab_name]["calc_comboBox"].update_idletasks()

    ##### Applied / notApplied_famType_sheetview 우측 영역 업데이트 구간

    if state.selected_calcType_name.get() != "Selected Calc Type: ":
        items = state.project_info.get("calc_types", [])
        calcType_names = list(
            map(
                lambda x: x["type_tag"],
                filter(lambda x: x["category"] == tab_name, items),
            )
        )
        state[tab_name]["selected_calcType_name"].set(
            "Selected Calc Type: " + calcType_names[0]
        )

    state.logging_text_widget.write(
        "::: 현재 작업 빌딩 : " + selected_building + " :::"
    )

    applied_famType_sheetview = state[tab_name]["applied_famType_sheetview"]

    apply_target_rvtTypes = state.project_info["apply_target_rvtTypes"][tab_name]

    applied_famType_sheetview.clear()

    idxs = range(len(apply_target_rvtTypes))
    applies = []
    not_applies = []
    for rowidx in idxs:
        if (
            apply_target_rvtTypes[rowidx]["bd_tag"] == selected_building
            and apply_target_rvtTypes[rowidx]["stdType_tag"] == selected_type_name
        ):
            # apply_target_rooms[rowidx][
            #     "calc_tag"
            # ] = state.selected_calcType_name.get().split(": ")[-1]
            applies.append(
                [
                    apply_target_rvtTypes[rowidx]["rvtType_name"],
                    apply_target_rvtTypes[rowidx]["stdType_tag"],
                    apply_target_rvtTypes[rowidx]["bd_tag"],
                    apply_target_rvtTypes[rowidx]["calc_tag"],
                ]
            )

    applied_famType_sheetview.set_sheet_data(applies)

    applied_famType_sheetview.column_width(0, 170)
    applied_famType_sheetview.column_width(1, 150)


def update_selected_calcType_allCat(
    event,
    state,
    calc_comboBox,
    selected_calcType_sheetview,
    tab_name=None,
):
    if calc_comboBox.get():
        selected_calcType = calc_comboBox.get()
        state[tab_name]["selected_calcType_name"].set(
            "Selected Calc Type: " + selected_calcType
        )

    else:
        selected_calcType = (
            state[tab_name]["selected_calcType_name"].get().split(": ")[-1]
        )
    selectedCalcDic = list(
        filter(
            lambda x: x["type_tag"] == selected_calcType,
            state.project_info["calc_types"],
        )
    )[0]
    selectedCalc_model_params = selectedCalcDic["model_params"]
    selectedCalc_manual_params = selectedCalcDic["manual_params"]
    selectedCalc_params = selectedCalc_model_params + selectedCalc_manual_params
    selected_calcType_sheetview.set_sheet_data()
    paramDatas = []
    for param_dic in selectedCalc_params:
        c1 = param_dic["항목"]
        c2 = param_dic["수식 약자"]
        c3 = param_dic.get("수동입력값", "byRevit")
        paramDatas.append([c1, c2, c3])
    selected_calcType_sheetview.set_sheet_data(paramDatas)


def open_teamSTDtree_view_allCat(event, state):
    from src.views.tree_management import create_family_standard_tab

    window = tk.Toplevel()
    window.geometry("1280x800+100+100")
    window.wm_attributes("-topmost", 1)

    # create_calc_criteria_tab(window, state, mode="newWindow_room")
    create_family_standard_tab(window, None, state, mode="newWindow")


def open_calcType_view_allCat(event, state, tab_name):
    from src.tabs.calc_criteria_tab.calc_criteria_tab import create_calc_criteria_tab

    def select_item_by_value(treeview, column, value):
        # Iterate over all items in the treeview
        for child in treeview.get_children():
            # Get the value of the specified column for the current item
            item_value = treeview.item(child, "values")[column]
            # print(item_value)
            # If the value matches, select the item
            # print(item_value == value)
            if item_value == value:
                treeview.focus(child)
                treeview.selection_set(child)  ## 제대로 작동 안함. 확인 필요
                treeview.event_generate("<<TreeviewSelect>>")
                # print(treeview.event_generate("<<TreeviewSelect>>"))
                treeview.see(child)  # Scroll to the selected item if needed
                break  # Exit after the first match is found

    window = tk.Toplevel()
    window.geometry("1280x800+100+100")
    window.wm_attributes("-topmost", 1)

    create_calc_criteria_tab(window, state, mode="newWindow_room")
    selected_calcType = state[tab_name]["selected_calcType_name"].get().split(": ")[-1]

    select_item_by_value(state.cat_treeview, column=0, value=tab_name)
    select_item_by_value(
        state.calcType_treeview, column=0, value=selected_calcType.strip()
    )


# Function to update the second cell dropdown (B1) based on the first cell selection
def update_second_cell_dropdown_allCat(event, state, sheet):
    all_row_index = list(range(sheet.get_total_rows()))
    # print(all_row_index)

    # print(second_dropdowns)
    # Set the second cell's dropdown based on the first cell's value
    def update_unitCell_inRow(idx):
        if sheet.get_cell_data(idx, 4):
            selected_value = sheet.get_cell_data(idx, 4)
            unit_info = selected_value.split("... | ...")[-4]
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


def on_change_wmSheet_allCat(event, state, sheet, tab_name, mode=None):
    # update_second_cell_dropdown(event, state, sheet)
    if mode == "stdType":

        selected_stdType_name = (
            state[tab_name]["selected_stdType_name"].get().split(": ")[-1]
        )
        print(selected_stdType_name)
        state.logging_text_widget.write(selected_stdType_name)

        # sheet_kind = sheet.headers()[0]
        # print(sheet_kind)

        wmBunches = []
        for row in sheet.get_sheet_data():
            wm_row_dic = dict(zip(state[tab_name]["common_headers"], row))
            wmBunches.append(wm_row_dic)
        # print(wmBunches)
        # print(state.project_info["std_wm_assign_allCat"])

        # state.wmBunches_room = {}
        if state.project_info["std_wm_assign_allCat"][tab_name].get(
            selected_stdType_name
        ):
            state.project_info["std_wm_assign_allCat"][tab_name][
                selected_stdType_name
            ] = wmBunches
            # print(wmBunches)
            # print(state.project_info["std_wm_assign_allCat"])
        else:
            # state.wmBunches_room.update({sheet_kind: wmBunches})
            # state.project_info["std_wm_assign"] = {}
            state.project_info["std_wm_assign_allCat"][tab_name].update(
                {selected_stdType_name: wmBunches}
            )
            # print(state.project_info["std_wm_assign_allCat"])

        # state.logging_text_widget.write(("\n").join(list(map(str, wmBunches))))
    elif mode == "rvtType":

        selected_rvtType_name = state[tab_name]["selected_rvtType_name"].get()
        print(selected_rvtType_name)
        state.logging_text_widget.write(selected_rvtType_name)

        # sheet_kind = sheet.headers()[0]
        # print(sheet_kind)

        wmBunches = []
        for row in sheet.get_sheet_data():
            wm_row_dic = dict(zip(state[tab_name]["common_headers"], row))
            wmBunches.append(wm_row_dic)
        # print(wmBunches)

        # state.wmBunches_room = {}
        if state.project_info["apply_target_rvtTypes"][tab_name].get(
            selected_rvtType_name
        ):
            state.project_info["apply_target_rvtTypes"][tab_name][
                selected_rvtType_name
            ] = wmBunches
            # print(wmBunches)
            print(state.project_info["apply_target_rvtTypes"])
        else:
            # state.wmBunches_room.update({sheet_kind: wmBunches})
            # state.project_info["std_wm_assign"] = {}
            state.project_info["apply_target_rvtTypes"][tab_name].update(
                {selected_rvtType_name: wmBunches}
            )
            print(state.project_info["apply_target_rvtTypes"])

        # state.logging_text_widget.write(("\n").join(list(map(str, wmBunches))))


def add_assignRow_allCat(event, state, sheet, tab_name=None, dropdowns=None):
    if not dropdowns:
        dropdowns = list(state.wm_group_data.keys())
        # dropdowns = [1, 2, 3, 4, 5]
        # state.logging_text_widget.write(str(dropdowns))

    new_row_index = sheet.get_total_rows()  # Get the current total rows
    if state[tab_name]["stdTypeTree"].selection():
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


def create_tksheet_stdTypeWM(
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
    sheet.set_column_widths(state[tab_name]["common_widths"])

    sheet.extra_bindings(
        [
            (
                "rc_insert_row",
                lambda e: add_assignRow_allCat(e, state, sheet, tab_name=tab_name),
            ),
            (
                "rc_delete_row",
                lambda e: on_change_wmSheet_allCat(
                    e, state, sheet, tab_name, mode="stdType"
                ),
            ),
            (
                "end_edit_cell",
                # lambda e: update_second_cell_dropdown(e, state, sheet),
                lambda e: on_change_wmSheet_allCat(
                    e, state, sheet, tab_name, mode="stdType"
                ),
            ),
            (
                "cell_select",
                lambda e: update_second_cell_dropdown_allCat(e, state, sheet),
            ),
        ]
    )

    return sheet


def create_tksheet_revitWM(
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

    sheet.extra_bindings(
        [
            (
                "rc_insert_row",
                lambda e: add_assignRow_allCat(e, state, sheet, tab_name=tab_name),
            ),
            (
                "rc_delete_row",
                lambda e: on_change_wmSheet_allCat(e, state, sheet, tab_name),
            ),
            (
                "end_edit_cell",
                # lambda e: update_second_cell_dropdown(e, state, sheet),
                lambda e: on_change_wmSheet_allCat(e, state, sheet, tab_name),
            ),
            (
                "cell_select",
                lambda e: update_second_cell_dropdown_allCat(e, state, sheet),
            ),
        ]
    )

    return sheet


def update_combobox_data_other(state, data, tab_name=None):
    """
    Update the combobox values based on the data loaded from the JSON file.
    """
    #####################
    #### building combobox
    bd_combobox = state[tab_name]["bd_combobox"]

    building_items = data.get("building_list", [])
    building_names = list(map(lambda x: x["building_name"], building_items))

    # Update the combobox values
    bd_combobox["values"] = ["프로젝트 공통"] + building_names

    # Set the default value to the first item if available
    if building_names and state.selected_building != "대상 빌딩 선택":
        bd_combobox.set(state.selected_building)
        # print(type(state.selected_building))
        print(state.selected_building)
        pass
    elif building_names and not state.selected_building:
        bd_combobox.set("대상 빌딩 선택")
    else:
        bd_combobox.set("")  # Clear the combobox if no items are available

    #####################
    ### calc combobox
    calc_combobox = state[tab_name]["calc_comboBox"]
    calc_items = data.get("calc_types", [])
    calcType_names = list(
        map(
            lambda x: x["type_tag"],
            filter(lambda x: x["category"] == tab_name, calc_items),
        )
    )

    # Update the combobox values
    calc_combobox["values"] = calcType_names

    # Set the default value to the first item if available
    if calcType_names:
        calc_combobox.set(calcType_names[0])
    else:
        calc_combobox.set("")  # Clear the combobox if no items are available


def update_stdTypeTree_otherCat(event, state, tab_name, mode=None):
    bd_comboBox = state[tab_name]["bd_combobox"]
    state.selected_building = bd_comboBox.get()
    # print(type(state.selected_building))
    print(state.selected_building)

    update_selected_calcType_allCat(
        event,
        state,
        state[tab_name]["calc_comboBox"],
        state[tab_name]["selected_calcType_sheetview"],
        tab_name=tab_name,
    )

    def find_stdType_items_inCat(cat, state):
        def find_level_5_items(
            node,
            level=1,
        ):
            # Initialize an empty list to store level 5 items
            level_5_items = []

            # Check if the current node is a level 5 item by counting dots in 'number'
            if node.get("number", "").count(".") == 4:
                # Initialize the wmGrp list to store level 7 item names
                wmGrps = []

                # Define a helper function to find all level 7 items under the current level 5 item
                def find_level_7_names(sub_node, sub_level):
                    # Check if the current level is 7 (3 levels deeper than level 5)
                    if sub_level == 7:
                        wmGrps.append(sub_node.get("name"))
                    # If there are children, continue to traverse deeper
                    if "children" in sub_node:
                        for child in sub_node["children"]:
                            find_level_7_names(child, sub_level + 1)

                # Find all level 7 item names under this level 5 item
                find_level_7_names(node, level)

                level_5_items.append(
                    {
                        "name": node.get("name"),
                        "number": node.get("number"),
                        "description": node.get("description"),
                        "wmGrps": wmGrps,
                    }
                )

            # If the node has children, iterate over them and recurse
            if "children" in node:
                for child in node["children"]:
                    level_5_items.extend(find_level_5_items(child, level + 1))
            # print(level_5_items)
            return level_5_items

        lv_5_items = []
        for root_node in state.stdTypes_info:
            if root_node["name"] == cat:
                lv_5_items.extend(find_level_5_items(root_node))
        if state.project_info.get("std_types").get(tab_name):
            pass
        else:
            state.project_info["std_types"] = {
                tab_name: list(
                    map(
                        lambda x: {
                            "std_type": x["name"],
                            "building_tag": "",
                            "cat_tag": tab_name,
                            "wmGrps": x["wmGrps"],
                        },
                        lv_5_items,
                    )
                )
            }
        return lv_5_items

    if not state.project_info.get("std_types"):
        find_stdType_items_inCat(tab_name, state)

    stdType_items = state.project_info["std_types"][tab_name]

    if mode == "loading" and not state.selected_stdType:
        state[tab_name]["stdTypeTree"].delete(
            *state[tab_name]["stdTypeTree"].get_children()
        )

        for dic in stdType_items:
            print(dic)
            state[tab_name]["stdTypeTree"].insert("", "end", values=list(dic.values()))


def add_to_appliedRvtType_data(state, revit_famType_input, tab_name=None):
    # selected_items = state.notApplied_famType_sheetview.get_currently_selected()
    input_items = list(
        map(
            lambda x: x.strip(),
            revit_famType_input.get("1.0", tk.END).strip().split("\n"),
        )
    )
    print(input_items)

    def add_oneRow(input_item):
        # selectedRow = input_item[0]
        rvt_type = input_item
        if not state.project_info.get("apply_target_rvtTypes"):
            state.project_info["apply_target_rvtTypes"] = {tab_name: []}

        if rvt_type not in state.project_info["apply_target_rvtTypes"][tab_name]:
            state.project_info["apply_target_rvtTypes"][tab_name].append(
                {
                    "rvtType_name": rvt_type,
                    "stdType_tag": state[tab_name]["selected_stdType_name"]
                    .get()
                    .split(": ")[-1],
                    "bd_tag": state.selected_building,
                    "calc_tag": state[tab_name]["selected_calcType_name"]
                    .get()
                    .split(": ")[-1],
                    "rvt_only_wm": [],
                }
            )

        applied_rvtTypes = state[tab_name]["applied_famType_sheetview"].get_sheet_data()
        for rvtType_dic in state.project_info["apply_target_rvtTypes"][tab_name]:
            if rvtType_dic["rvtType_name"] == rvt_type:
                applied_rvtTypes.append(
                    [
                        rvtType_dic["rvtType_name"],
                        rvtType_dic["stdType_tag"],
                        rvtType_dic["bd_tag"],
                        rvtType_dic["calc_tag"],
                    ]
                )
        state[tab_name]["applied_famType_sheetview"].set_sheet_data(applied_rvtTypes)

    if state.selected_building == "대상 빌딩 선택":
        print(state.selected_building)
        state.logging_text_widget.write("!!! 화면 상단에서 빌딩을 선택해 주세요 !!!")
    elif not state[tab_name]["selected_rvtType_name"].get():
        state.logging_text_widget.write("!!! 스탠다드 타입을 선택해 주세요 !!!")
    else:
        for input_item in input_items:
            add_oneRow(input_item)

    revit_famType_input.delete("1.0", tk.END)
    state[tab_name]["applied_famType_sheetview"].column_width(0, 170)
    state[tab_name]["applied_famType_sheetview"].column_width(1, 150)


def remove_from_appliedRvtType_data(state, revit_famType_input, tab_name=None):
    selected_items = list(
        state[tab_name]["applied_famType_sheetview"].get_selected_cells()
    )

    def remove_oneRow(selected_item):
        # selectedRow = selected_item.row
        selectedRow = selected_item[0]
        rvt_type = state[tab_name]["applied_famType_sheetview"].get_cell_data(
            selectedRow, 0
        )
        print(rvt_type)
        # removed_items.append(rvt_type)
        copied_rvt_type = deepcopy(rvt_type)
        for idx, rvtType_dic in enumerate(
            state.project_info["apply_target_rvtTypes"][tab_name]
        ):
            if rvtType_dic["rvtType_name"] == rvt_type:
                state.logging_text_widget.write(str(rvtType_dic))
                del state.project_info["apply_target_rvtTypes"][tab_name][idx]

        return copied_rvt_type

    removed_items = []
    for selected_item in selected_items:
        removed = remove_oneRow(selected_item)
        removed_items.append(removed)

    removed_texts = "\n".join(removed_items)
    # print(removed_items)
    revit_famType_input.insert("1.0", removed_texts)
    # print(selected_items)
    selected_items_rows = list(map(lambda x: x[0], selected_items))
    state[tab_name]["applied_famType_sheetview"].delete_rows(selected_items_rows)

    state.applied_famType_sheetview.column_width(0, 170)
    state.applied_famType_sheetview.column_width(1, 150)
