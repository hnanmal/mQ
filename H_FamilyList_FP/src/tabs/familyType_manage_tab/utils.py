# src/tabs/familyType_manage_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# from src.tabs.input_common_tab.utils import create_defaultTreeview


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
