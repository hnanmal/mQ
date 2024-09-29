# src/tabs/familyType_manage_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# from src.tabs.input_common_tab.utils import create_defaultTreeview


def on_doubleClick_newWindow(event, state, calcType_treeview):
    window = tk.Toplevel()
    window.geometry("640x800+100+100")
    window.wm_attributes("-topmost", 1)

    section1_window = ttk.Frame(window, width=800, height=100)
    section1_window.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=True)

    std_type_label_pre = ttk.Label(
        section1_window, text="Standard Type List by standard", font=("Arial", 14)
    )
    std_type_label_pre.pack(pady=10, fill=tk.BOTH, expand=True)

    ### search 영역
    search_var = tk.StringVar()
    search_label = ttk.Label(section1_window, text="Search", font=("Arial", 11))
    search_label.pack(padx=5, anchor="w")
    search_entry = ttk.Entry(section1_window, textvariable=search_var)
    search_entry.pack(padx=5, anchor="w")

    # Bind the Enter key to trigger search functionality
    search_entry.bind(
        "<Return>",
        lambda event: search_stdTypes(
            sheet_widget,
            data,
            search_var.get(),
        ),
    )

    # section4_window = ttk.Frame(window, width=800, height=100)
    # section5_window = ttk.Frame(window, width=800, height=100)
    # section4_window.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=True)
    # section5_window.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

    stdTypes_preListbox = tk.Listbox(section1_window, selectmode=tk.SINGLE, height=20)
    stdTypes_preListbox.pack(padx=5, anchor="w")

    # # Section 4 - Selected Calc types's Model Parameter list
    # modelParam_label = ttk.Label(
    #     section4_window, text="모델 Parameter", font=("Arial", 14, "bold")
    # )
    # modelParam_label.pack(padx=20, pady=10, anchor="w")

    # modelParam_treeview_frame = ttk.Frame(section4_window, width=300, height=100)
    # modelParam_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # modelParam_treeview_window = create_defaultTreeview(
    #     state,
    #     modelParam_treeview_frame,
    #     ("항목", "수식 약자", "Parameter", "단위", "비고", "calc_type"),
    #     height=5,
    # )
    # modelParam_treeview_window.pack(pady=10, fill=tk.X, expand=True)

    # modelParam_treeview_window.bind(
    #     "<Double-Button-1>",
    #     lambda e: on_click_edit_modelParam(
    #         e,
    #         state,
    #         modelParam_treeview_window,
    #         calcType_treeview,
    #     ),
    # )

    # new_modelParam_text = tk.Text(section4_window, height=2, width=100)
    # new_modelParam_text.pack(side=tk.RIGHT, pady=5, anchor="e")

    # add_new_modelParam_button = ttk.Button(
    #     section4_window,
    #     text="Add",
    #     command=lambda: add_modelParam(
    #         state, calcType_treeview, modelParam_treeview_window, new_modelParam_text
    #     ),
    # )
    # add_new_modelParam_button.pack(side=tk.LEFT, padx=5, pady=5)

    # del_selected_modelParam_button = ttk.Button(
    #     section4_window,
    #     text="Del",
    #     command=lambda: remove_modelParam(
    #         state, modelParam_treeview_window, calcType_treeview
    #     ),
    # )
    # del_selected_modelParam_button.pack(side=tk.LEFT, padx=5, pady=5)


def search_stdTypes():
    pass


def create_stdTypes_listbox():
    pass


def update_checkCanvas_data(
    state,
    checkCanvas,
    data,
    selected_building,
    cat=None,
):
    """
    Update the checkCanvas values based on the data loaded from the JSON file.
    """
    selected_building = state.current_selected_building
    if cat == "Room":
        items = data.get("building_list", [])
        stdType_names = list(
            map(
                lambda x: list(map(lambda y: y["finish_type"], x["room_list"])),
                filter(
                    lambda x: x["building_name"] == selected_building,
                    items,
                ),
            )
        )[0]
        print(stdType_names)
        checkCanvas.set_data(state, stdType_names)

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
