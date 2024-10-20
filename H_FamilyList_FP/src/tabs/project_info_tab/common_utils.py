# src/views/project_info_tab/common_utils.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

from src.tabs.familyType_manage_tab.utils import (
    update_combobox_data,
    update_notAppliedRoom_data,
    update_selected_calcType,
    update_stdTypeTree_inRoom,
)
from src.tabs.familyType_manage_tab.otherTabs.utils import (
    update_combobox_data_other,
    update_stdTypeTree_otherCat,
)


def refresh_treeview(treeview, data, targetCat):
    # Clear existing Treeview data
    treeview.delete(*treeview.get_children())
    # Insert new data from the loaded JSON
    for item in data.get("common_info", {}).get(targetCat, []):
        treeview.insert(
            "",
            "end",
            values=(
                item["항목"],
                item["입력값"],
                item["단위"],
                item["비고"],
            ),
        )


# Load Project Info Button
def load_project_info(
    state,
    project_name_var,
    project_type_var,
    building_treeview,
    earth_treeview,
    steel_treeview,
    file_path_arg=None,
):
    state.project_name_var = project_name_var
    state.project_type_var = project_type_var
    if file_path_arg:
        file_path = file_path_arg
    else:
        file_path = filedialog.askopenfilename(filetypes=[("BNOTE files", "*.bnote")])
        # if file_path:
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    # Save loaded data to state
    state.project_info = loaded_data
    state["current_loaded_pjt"].set(file_path)
    # print(state.project_info)

    # Update the Treeview with loaded data
    refresh_treeview(earth_treeview, loaded_data, "earth")
    refresh_treeview(steel_treeview, loaded_data, "steel")

    # Populate UI fields from project_info
    project_name_var.set(loaded_data.get("project_name", ""))
    project_type_var.set(loaded_data.get("project_type", ""))

    # Clear and populate the building treeview
    building_treeview.delete(*building_treeview.get_children())
    for building_data in loaded_data.get("building_list", []):
        building_treeview.insert(
            "",
            "end",
            values=(
                building_data["building_name"],
                building_data["building_number"],
            ),
        )

    update_notAppliedRoom_data(state)
    update_combobox_data(state, state.bd_combobox_room, loaded_data, "building")
    update_combobox_data(state, state.calc_comboBox_room, loaded_data, "calc", "Room")
    update_stdTypeTree_inRoom(None, state, state.bd_combobox_room, "loading")

    update_combobox_data_other(state, loaded_data, "Floors")
    update_stdTypeTree_otherCat(None, state, "Floors", "loading")

    print(state.selected_building)
    # if state.selected_building:
    #     state.bd_combobox_room.set(state.selected_building)
    state.bd_combobox_room.set(state.selected_building)

    state.logging_text_widget.write(f"Project Info loaded from {file_path}\n")


def save_project_info(
    state,
    project_name_var,
    project_type_var,
):
    # Save project_info in the state
    state.project_info["project_name"] = project_name_var.get()
    state.project_info["project_type"] = project_type_var.get()
    project_info_ = state.project_info

    # Save to file
    # file_path = f"{project_info_['project_name']}_pjt_info.json"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".bnote",  # Default file extension
        filetypes=[("BNOTE files", "*.bnote"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")

    load_project_info(
        state,
        project_name_var,
        project_type_var,
        state.building_treeview,
        state.earth_treeview,
        state.steel_treeview,
        file_path_arg=file_path,
    )


# Function to handle in-place editing
def on_click_edit(event, state, tree):

    # Identify which item and column were clicked
    region = tree.identify_region(event.x, event.y)
    if region == "cell":
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)

        # Get the item ID and current value of the clicked cell
        item_id = tree.identify_row(event.y)
        col_num = (
            int(column.replace("#", "")) - 1
        )  # Treeview columns are numbered as #1, #2, ...
        current_value = tree.item(item_id, "values")[col_num]

        # Get the bounding box of the cell
        x, y, width, height = tree.bbox(item_id, column)

        # Create an Entry widget over the cell
        entry = ttk.Entry(tree)
        entry.place(x=x, y=y, width=width, height=height)

        # Insert the current value into the Entry widget
        entry.insert(0, current_value)
        entry.focus()

        # Save the new value when Enter is pressed or focus is lost
        def save_edit(state, event=None):
            new_value = entry.get()
            values = list(tree.item(item_id, "values"))
            values[col_num] = new_value
            tree.item(item_id, values=values)  # Update the treeview with the new value
            entry.destroy()  # Remove the Entry widget after saving
            state.edited_value.set(new_value)
            print(state.edited_value.get())
            # return new_value

        entry.bind(
            "<Return>", lambda e: save_edit(state, e)
        )  # Save when Enter is pressed
        entry.bind(
            "<FocusOut>", lambda e: save_edit(state, e)
        )  # Save when focus is lost
