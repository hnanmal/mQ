from src.utils.fp_utils import *
from src.tabs.familyType_manage_tab.utils import update_selected_calcType
import tkinter as tk
from tksheet import Sheet
from copy import copy
from copy import deepcopy


def on_right_click_stdTypetree_otherTab(event, state, tree, tab_name):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if item and column:
        menu = generate_context_menu_otherTab(state, tree, item, column, tab_name)
        menu.post(event.x_root, event.y_root)


def generate_context_menu_otherTab(state, tree, item, column, tab_name):
    menu = tk.Menu(tree, tearoff=0)
    actions = {
        "Edit": lambda: enable_tree_item_editing_otherTab(
            state, tree, item, column, tab_name
        ),
        "Delete": lambda: del_stdType_allCat(state),
        # Additional actions...
    }

    for label, command in actions.items():
        menu.add_command(label=label, command=command)

    return menu


def enable_tree_item_editing_otherTab(state, tree, item, column, tab_name):
    """Enable editing for the specified column of the treeview item."""
    x, y, width, height = tree.bbox(item, column)
    entry = tk.Entry(tree, width=width)

    oldType_name = tree.item(item, "values")[0]
    oldBd_tag = tree.item(item, "values")[1]

    def save_edit(event, column):
        new_value = entry.get()
        tree.set(item, column=column, value=new_value)
        entry.destroy()

        if column == "#2":
            for std_dic in state.project_info["std_types"][tab_name]:
                if (
                    std_dic["std_type"] == oldType_name
                    and std_dic["building_tag"] == oldBd_tag
                ):
                    std_dic["std_type"] = new_value

            ## 변한 키이름을 state.project_info["std_wm_assign"]에 연동
            state.project_info["std_wm_assign_allCat"][tab_name][new_value] = (
                state.project_info["std_wm_assign_allCat"].pop(oldType_name)
            )

            ## 변한 키이름을 state.project_info["apply_target_rooms"]에 연동
            for rvtType_dic in state.project_info["apply_target_rvtTypes"][tab_name]:
                if rvtType_dic["stdType_tag"] == oldType_name:
                    rvtType_dic["stdType_tag"] = new_value

        elif column == "#3":
            for std_dic in state.project_info["std_types"][tab_name]:
                if (
                    std_dic["std_type"] == oldType_name
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


def update_unitCell_inRow(state, sheet, row_idx):
    [WM_col_idx, unit_col_idx, wmGrp_col_idx, desc_col_idx] = state.idxes
    if sheet.get_cell_data(row_idx, WM_col_idx):
        selected_value = sheet.get_cell_data(row_idx, WM_col_idx)
        unit_info = selected_value.split(" | ")[-4]
        sheet.set_cell_data(row_idx, unit_col_idx, unit_info)


def update_descriptionCell_inRow(state, sheet, row_idx):
    [WM_col_idx, unit_col_idx, wmGrp_col_idx, desc_col_idx] = state.idxes
    if (
        sheet.get_cell_data(row_idx, WM_col_idx)
        and sheet.get_cell_data(row_idx, desc_col_idx) == ""
    ):
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


def fill_wm(state, sheet, row_idx, wmGrp_col_idx, WM_col_idx):
    if "공통|" in sheet.get_cell_data(row_idx, wmGrp_col_idx):
        common_WM_values = list(
            chain(*state.project_info["common_items_info"].values())
        )
        # print(common_WM_values)
        tgt_common_WM_value = go(
            common_WM_values,
            filter(lambda x: x.get("wmGrp")),
            filter(lambda x: x["wmGrp"] == sheet.get_cell_data(row_idx, wmGrp_col_idx)),
            list,
            lambda x: x[0],
            lambda x: x.values(),
            list,
        )[1:]
        tgt_common_WM_value.insert(1, "")
        # print(tgt_common_WM_value)
        for col_idx, x in enumerate(tgt_common_WM_value):
            if col_idx != 1:  ## 산출수식 초기화 방지
                sheet.set_cell_data(row_idx, col_idx, x)
                sheet.del_dropdown(row_idx, WM_col_idx)  ## 공통 항목은 드롭다운 제거
    else:
        pass


def update_row(state, sheet, row_idx):
    [WM_col_idx, unit_col_idx, wmGrp_col_idx, desc_col_idx] = state.idxes
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
    second_dropdowns = go(
        second_dropdowns_obj["matched_items"],
        map(lambda x: x.split(" | ")),
        map(lambda x: filter(lambda y: y != "0", x)),
        map(lambda x: filter(lambda y: y != "", x)),
        map(lambda x: " | ".join(x)),
        list,
    )

    if not current_WM_value:
        # second_dropdowns = second_dropdowns_obj["matched_items"]
        sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
        update_unitCell_inRow(state, sheet, row_idx)
        update_descriptionCell_inRow(state, sheet, row_idx)
        fill_wm(state, sheet, row_idx, wmGrp_col_idx, WM_col_idx)
    elif current_WM_value == second_dropdowns_obj["matched_items"][0]:
        sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
        update_descriptionCell_inRow(state, sheet, row_idx)
        fill_wm(state, sheet, row_idx, wmGrp_col_idx, WM_col_idx)
    elif current_WM_value != second_dropdowns_obj["matched_items"][0]:
        sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
        sheet.set_cell_data(row_idx, WM_col_idx, current_WM_value)
        update_descriptionCell_inRow(state, sheet, row_idx)
        fill_wm(state, sheet, row_idx, wmGrp_col_idx, WM_col_idx)
    elif current_WM_value not in second_dropdowns_obj["matched_items"]:
        sheet.create_dropdown(row_idx, WM_col_idx, values=second_dropdowns)
        update_descriptionCell_inRow(state, sheet, row_idx)
        fill_wm(state, sheet, row_idx, wmGrp_col_idx, WM_col_idx)
    else:
        update_descriptionCell_inRow(row_idx)
        fill_wm(state, sheet, row_idx, wmGrp_col_idx, WM_col_idx)
        pass


def add_stdType_allCat(state, new_stdType_text, tab_name):
    stdType_input = new_stdType_text.get("1.0", tk.END).strip()
    if stdType_input:
        stdTypes = stdType_input.split("\n")
        for stdType in stdTypes:
            if stdType.strip():
                stdType_name = stdType.strip()
                state.project_info["std_types"][tab_name].append(
                    {
                        "parent_type": "",
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
        selected_type_name = current_selected_stdType.get("values")[1]
        if state.project_info["std_wm_assign_allCat"].get(tab_name):
            if state.project_info["std_wm_assign_allCat"][tab_name].get(
                selected_type_name
            ):
                WMsheet.set_column_widths(state[tab_name]["common_widths"])
                pass
            else:
                init_WMsheetviews(state, WMsheet, selected_type_name)
        else:
            state.project_info["std_wm_assign_allCat"][tab_name] = {}
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
        for row_idx in list(range(len(data))):
            update_row(state, sheet, row_idx)

    if not state.project_info.get("std_wm_assign_allCat"):
        state.project_info["std_wm_assign_allCat"] = {}
        state.project_info["std_wm_assign_allCat"][tab_name] = {}

    if state.project_info["std_wm_assign_allCat"][tab_name].get(selected_type_name):
        data_dic = state.project_info["std_wm_assign_allCat"][tab_name][
            selected_type_name
        ]
        data = list(map(lambda x: list(x.values()), data_dic))
        # print(data)
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

    if state.project_info["apply_target_rvtTypes"].get(tab_name):
        apply_target_rvtTypes = state.project_info["apply_target_rvtTypes"][tab_name]
    else:
        state.project_info["apply_target_rvtTypes"] = {tab_name: []}
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
    # calc_comboBox,
    selected_calcType_sheetview,
    tab_name=None,
):
    calc_comboBox = state[tab_name]["calc_comboBox"]
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
    window.wm_attributes("-topmost", False)

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
    window.wm_attributes("-topmost", False)

    create_calc_criteria_tab(window, state, mode="newWindow_room")
    selected_calcType = state[tab_name]["selected_calcType_name"].get().split(": ")[-1]

    select_item_by_value(state.cat_treeview, column=0, value=tab_name)
    select_item_by_value(
        state.calcType_treeview, column=0, value=selected_calcType.strip()
    )


# Function to update the second cell dropdown (B1) based on the first cell selection
def update_second_cell_dropdown_allCat(event, state, sheet):
    all_row_index = list(range(sheet.get_total_rows()))

    for idx in all_row_index:
        update_row(state, sheet, idx)
        # update_unitCell_inRow(idx)


def on_change_wmSheet_allCat(event, state, sheet, tab_name, mode=None):
    # update_second_cell_dropdown(event, state, sheet)
    if mode == "stdType":

        selected_stdType_name = (
            state[tab_name]["selected_stdType_name"].get().split(": ")[-1]
        )
        print(selected_stdType_name)
        state.logging_text_widget.write(selected_stdType_name)

        wmBunches = []
        for row in sheet.get_sheet_data():
            wm_row_dic = dict(zip(state[tab_name]["common_headers"], row))
            wmBunches.append(wm_row_dic)

        if state.project_info["std_wm_assign_allCat"][tab_name].get(
            selected_stdType_name
        ):
            state.project_info["std_wm_assign_allCat"][tab_name][
                selected_stdType_name
            ] = wmBunches

        else:
            state.project_info["std_wm_assign_allCat"][tab_name].update(
                {selected_stdType_name: wmBunches}
            )
        # state.logging_text_widget.write(("\n").join(list(map(str, wmBunches))))

    elif mode == "rvtType":

        selected_rvtType_name = state[tab_name]["selected_rvtType_name"].get()
        print(selected_rvtType_name)
        state.logging_text_widget.write(selected_rvtType_name)

        wmBunches = []
        for row in sheet.get_sheet_data():
            wm_row_dic = dict(zip(state[tab_name]["common_headers"], row))
            wmBunches.append(wm_row_dic)

        if state.project_info["apply_target_rvtTypes"][tab_name].get(
            selected_rvtType_name
        ):
            state.project_info["apply_target_rvtTypes"][tab_name][
                selected_rvtType_name
            ] = wmBunches
        else:
            state.project_info["apply_target_rvtTypes"][tab_name].update(
                {selected_rvtType_name: wmBunches}
            )
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
    sheet.header_font(("Arial", 7, "normal"))
    sheet.set_options(
        font=("Arial Narrow", 8, "normal"), default_row_height=35
    )  # Font name and size

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
        # state[tab_name]["calc_comboBox"],
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

        print("find_stdType_items_inCat 작동확인")

        lv_5_items = []
        for root_node in state.stdTypes_info:
            if root_node["name"] == cat:
                lv_5_items.extend(find_level_5_items(root_node))
        # print(lv_5_items)

        if state.project_info["std_types"].get(tab_name):
            print(f"std_types 하위 {tab_name} 키 존재!")
            # print(state.project_info["std_types"][tab_name])
        else:
            print(f"std_types 하위 {tab_name} 키 미 존재! 키 신규 생성")
            state.project_info["std_types"][tab_name] = []
            state.project_info["std_types"][tab_name].extend(
                list(
                    map(
                        lambda x: {
                            "parent_type": "",
                            "std_type": x["name"],
                            "building_tag": "",
                            "cat_tag": tab_name,
                            "wmGrps": x["wmGrps"],
                        },
                        lv_5_items,
                    )
                )
            )
            # print(state.project_info["std_types"][tab_name])

        return lv_5_items

    # if not state.project_info.get("std_types"):
    #     find_stdType_items_inCat(tab_name, state)
    # if not state.project_info["std_types"].get(tab_name):
    #     find_stdType_items_inCat(tab_name, state)
    find_stdType_items_inCat(tab_name, state)

    if not state.project_info["apply_target_rvtTypes"].get(tab_name):
        state.project_info["apply_target_rvtTypes"][tab_name] = []

    assigned_from_apply_target = go(
        state.project_info["apply_target_rvtTypes"][tab_name],
        map(lambda dic: dic["stdType_tag"]),
        lambda x: set(x),
        list,
    )

    stdType_items = state.project_info["std_types"][tab_name]

    assigned_stdType_items = go(
        stdType_items,
        filter(lambda dic: dic["std_type"] in assigned_from_apply_target),
    )

    not_assigned_stdType_items = go(
        stdType_items,
        filter(lambda dic: dic["std_type"] not in assigned_from_apply_target),
    )

    if mode == "loading":  # and not state.selected_stdType:
        state[tab_name]["stdTypeTree"].delete(
            *state[tab_name]["stdTypeTree"].get_children()
        )

        for dic in assigned_stdType_items:
            # print(dic)
            state[tab_name]["stdTypeTree"].insert(
                "",
                "end",
                values=list(dic.values()),
            )
        for dic in not_assigned_stdType_items:
            # print(dic)
            state[tab_name]["stdTypeTree"].insert(
                "",
                "end",
                values=list(dic.values()),
                tag="highlight",
            )
    elif state[tab_name]["bd_combobox"].get():
        state[tab_name]["stdTypeTree"].delete(
            *state[tab_name]["stdTypeTree"].get_children()
        )

        try:
            assigned_from_apply_target_forBD = go(
                state.project_info["apply_target_rvtTypes"][tab_name],
                filter(
                    lambda dic: dic["bd_tag"] == state[tab_name]["bd_combobox"].get()
                ),
                map(lambda dic: dic["stdType_tag"]),
                lambda x: set(x),
                list,
            )
        except:
            assigned_from_apply_target_forBD = []

        assigned_stdType_items_forBD = go(
            stdType_items,
            filter(lambda dic: dic["std_type"] in assigned_from_apply_target_forBD),
            list,
        )
        not_assigned_stdType_items_forBD = go(
            stdType_items,
            filter(lambda dic: dic["std_type"] not in assigned_from_apply_target_forBD),
            list,
        )
        for dic in assigned_stdType_items_forBD:
            # print(dic)
            state[tab_name]["stdTypeTree"].insert(
                "",
                "end",
                values=list(dic.values()),
            )
        for dic in not_assigned_stdType_items_forBD:
            # print(dic)
            state[tab_name]["stdTypeTree"].insert(
                "",
                "end",
                values=list(dic.values()),
                tag="highlight",
            )

    state[tab_name]["stdTypeTree"].tag_configure(
        "highlight", background="#e3e3e3"
    )  # Light red background for highlight


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
