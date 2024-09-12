# src/views/project_info_tab/common_utils.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json


def save_project_info(state, project_name_var, project_type_var, building_treeview):
    # Consolidate all relevant data into the project_info dictionary
    project_info_ = {
        "project_name": project_name_var.get(),
        "project_type": project_type_var.get(),
        "building_list": {
            building_treeview.item(item, "values")[0]: {
                "building_name": building_treeview.item(item, "values")[0],
                "building_number": int(building_treeview.item(item, "values")[1])
                or None,
                "finish_types": state.project_info["building_list"][
                    building_treeview.item(item, "values")[0]
                ]["finish_types"]
                or [],
            }
            for item in building_treeview.get_children()
        },
    }

    # Save project_info in the state
    state.project_info = project_info_

    # Save to file
    file_path = f"{project_info_['project_name']}_pjt_info.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}")


# Load Project Info Button
def load_project_info(
    state, project_name_var, project_type_var, building_treeview, finish_listbox
):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        # Save loaded data to state
        state.project_info = loaded_data
        # print(state.project_info)

        # Populate UI fields from project_info
        project_name_var.set(loaded_data.get("project_name", ""))
        project_type_var.set(loaded_data.get("project_type", ""))

        # Clear and populate the building treeview
        building_treeview.delete(*building_treeview.get_children())
        # for building_name, building_data in loaded_data.get(
        #     "building_list", {}
        # ).items():
        #     building_treeview.insert(
        #         "",
        #         "end",
        #         values=(
        #             building_data["building_name"],
        #             building_data["building_number"],
        #         ),
        #     )
        for building_data in loaded_data.get(
            "building_list", []
        ):
            building_treeview.insert(
                "",
                "end",
                values=(
                    building_data["building_name"],
                    building_data["building_number"],
                ),
            )

        # Clear and populate finish types for the selected building
        finish_listbox.delete(0, tk.END)
        selected_building = building_treeview.selection()
        if selected_building:
            selected_building_name = building_treeview.item(
                selected_building[0], "values"
            )[0]
            finish_types = (
                loaded_data.get("building_list", {})
                .get(selected_building_name, {})
                .get("finish_types", [])
            )
            for finish_type in finish_types:
                finish_listbox.insert(tk.END, finish_type)

        state.logging_text_widget.write(f"Project Info loaded from {file_path}")
