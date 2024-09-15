# src/views/project_info_tab/common_utils.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json


def save_project_info(
    state, project_name_var, project_type_var, building_treeview, room_treeview
):
    # Consolidate all relevant data into the project_info dictionary
    # project_info_ = {
    #     "project_name": project_name_var.get(),
    #     "project_type": project_type_var.get(),
    #     "building_list": [
    #         {
    #             "building_name": building_treeview.item(item, "values")[0],
    #             "building_number": int(building_treeview.item(item, "values")[1])
    #             or None,
    #             "room_list": {}
    #         }
    #         for item in building_treeview.get_children()
    #     ],
    # }
    # project_info_ = {
    #     "project_name": project_name_var.get(),
    #     "project_type": project_type_var.get(),
    #     "building_list": [],
    # }
    # for bd in building_treeview.get_children():
    #     building_treeview.focus(bd)
    #     project_info_["building_list"].append(
    #         {
    #             "building_name": building_treeview.item(bd, "values")[0],
    #             "building_number": int(building_treeview.item(bd, "values")[1]),
    #             "room_list": [
    #                 {
    #                     "room_name": room_treeview.item(room, "values")[0],
    #                     "room_no": room_treeview.item(room, "text"),
    #                     "finish_type": room_treeview.item(room, "values")[1],
    #                 }
    #                 for room in room_treeview.get_children()
    #             ],
    #         }
    #     )

    # Save project_info in the state
    # state.project_info = project_info_
    state.project_info["project_name"] = project_name_var.get()
    state.project_info["project_type"] = project_type_var.get()
    project_info_ = state.project_info

    # Save to file
    # file_path = f"{project_info_['project_name']}_pjt_info.json"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Default file extension
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")


# Load Project Info Button
def load_project_info(
    state, project_name_var, project_type_var, building_treeview, room_treeview
):

    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        # Save loaded data to state
        state.project_info = loaded_data
        state["current_loaded_pjt"].set(f"<< {file_path} >> has been loaded !")
        # print(state.project_info)

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
        state.logging_text_widget.write(f"Project Info loaded from {file_path}\n")
