# src/tabs/familyType_manage_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def search_stdTypes():
    pass


def create_stdTypes_listbox():
    pass


def update_checkCanvas_data(checkCanvas, data, cat=None):
    """
    Update the checkCanvas values based on the data loaded from the JSON file.
    """
    if cat:
        items = data.get("calc_types", [])
        calcType_names = list(
            map(
                lambda x: x["type_tag"],
                filter(
                    lambda x: x["category"] == cat,
                    items,
                ),
            )
        )
        print(calcType_names)
        checkCanvas.set_data(calcType_names)

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
            combobox.set(building_names[0])
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
