import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

from src.views.project_info_tab.bd_treeview_utils import (
    add_building,
    auto_numbering,
    on_building_select,
    on_click_edit,
    remove_building,
)
from src.views.project_info_tab.common_utils import (
    # auto_numbering,
    load_project_info,
    save_project_info,
)
from src.views.project_info_tab.finishType_list_utils import (
    add_finish_type,
    remove_finish_type,
)


def create_project_info_tab(notebook, state):
    """Create the '프로젝트 정보 입력' tab with two sections."""
    project_info_tab = ttk.Frame(notebook)
    notebook.add(project_info_tab, text="프로젝트 정보 입력")

    # Divide the tab into three sections (frames)
    section1 = ttk.Frame(project_info_tab, width=300, height=200)
    section2 = ttk.Frame(project_info_tab, width=400, height=200)
    section3 = ttk.Frame(project_info_tab, width=400, height=200)

    section1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    section3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    section1.pack_propagate(False)
    section2.pack_propagate(False)
    section3.pack_propagate(False)

    save_load_btn_frame = ttk.Frame(section1, width=300)
    save_load_btn_frame.pack(pady=10, anchor="w")
    load_info_button = ttk.Button(
        save_load_btn_frame,
        text="Load Project Info",
        command=lambda: load_project_info(
            state, project_name_var, project_type_var, building_treeview, finish_listbox
        ),
    )
    load_info_button.pack(side="left", padx=30, pady=10, anchor="w")

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_info(
            state, project_name_var, project_type_var, building_treeview
        ),
    )
    save_info_button.pack(side="left", padx=30, pady=10, anchor="w")

    # Section 1 - Project Info
    project_name_label = ttk.Label(section1, text="Project Name", font=("Arial", 14))
    project_name_label.pack(pady=10, anchor="w")

    project_name_var = tk.StringVar()
    # state.project_name_var = project_name_var  ## state 전달
    project_name_entry = ttk.Entry(section1, textvariable=project_name_var, width=30)
    project_name_entry.pack(pady=10, anchor="w")

    # Project Type Label and Dropdown
    project_type_label = ttk.Label(section1, text="Project Type", font=("Arial", 14))
    project_type_label.pack(pady=10, anchor="w")

    project_type_var = tk.StringVar()
    # state.project_type_var = project_type_var  ## state 전달
    project_type_dropdown = ttk.Combobox(
        section1, textvariable=project_type_var, values=["Execution", "Bid"]
    )
    project_type_dropdown.pack(pady=10, anchor="w")

    # Building List Title
    building_list_label = ttk.Label(section1, text="Building List", font=("Arial", 14))
    building_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar
    bd_listbox_frame = ttk.Frame(section1, width=300)
    bd_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    auto_number_button = ttk.Button(
        bd_listbox_frame,
        text="Auto Numbering",
        command=lambda: auto_numbering(state, building_treeview),
    )
    auto_number_button.pack(side=tk.TOP, padx=5, pady=5, anchor="e")

    building_treeview = ttk.Treeview(
        bd_listbox_frame, columns=("Building Name", "Number"), show="headings", height=8
    )
    # state.building_treeview = building_treeview  ## state 전달

    building_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    building_treeview.heading("Building Name", text="Building Name")
    building_treeview.heading("Number", text="Number")

    building_treeview.column("Building Name", width=150)
    building_treeview.column("Number", width=100)

    scrollbar = ttk.Scrollbar(
        bd_listbox_frame, orient=tk.VERTICAL, command=building_treeview.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    building_treeview.config(yscrollcommand=scrollbar.set)

    new_building_text = tk.Text(section1, height=4, width=30)
    new_building_text.pack(pady=5, anchor="w")

    add_button = ttk.Button(
        section1,
        text="Add",
        command=lambda: add_building(state, building_treeview, new_building_text),
    )
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    remove_button = ttk.Button(
        section1,
        text="Remove",
        command=lambda: remove_building(state, building_treeview),
    )
    remove_button.pack(side=tk.LEFT, padx=5, pady=5)

    building_treeview.bind(
        "<Button-1>", lambda e: on_click_edit(e, state, building_treeview)
    )

    # Section 2 - Selected Building and Finish Type
    selected_building_label = ttk.Label(
        section2, text="Selected Building: ", font=("Arial", 14)
    )
    selected_building_label.pack(pady=10, anchor="w")

    finish_type_list_label = ttk.Label(
        section2, text="Finish Type List", font=("Arial", 14)
    )
    finish_type_list_label.pack(padx=20, pady=10, anchor="w")

    finish_listbox_frame = ttk.Frame(section2, width=300)
    finish_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    finish_listbox = tk.Listbox(finish_listbox_frame, height=8)
    finish_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    building_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: on_building_select(
            e, state, building_treeview, selected_building_label, finish_listbox
        ),
    )

    new_finish_text = tk.Text(finish_listbox_frame, height=2, width=30)
    new_finish_text.pack(pady=5)

    add_type_button = ttk.Button(
        finish_listbox_frame,
        text="Add Type",
        command=lambda: add_finish_type(
            state, building_treeview, finish_listbox, new_finish_text
        ),
    )
    add_type_button.pack(side=tk.LEFT, padx=5, pady=5)

    remove_type_button = ttk.Button(
        finish_listbox_frame,
        text="Remove Type",
        command=lambda: remove_finish_type(state, building_treeview, finish_listbox),
    )
    remove_type_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Section 3 - Room List
    selected_finishType_label = ttk.Label(
        section3, text="Selected finish Type: ", font=("Arial", 14)
    )
    selected_finishType_label.pack(pady=10, anchor="w")

    room_list_label = ttk.Label(section3, text="Room List", font=("Arial", 14))
    room_list_label.pack(padx=20, pady=10, anchor="w")

    room_listbox_frame = ttk.Frame(section3, width=300)
    room_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    room_listbox = tk.Listbox(room_listbox_frame, height=8)
    room_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    new_room_text = tk.Text(room_listbox_frame, height=2, width=30)
    new_room_text.pack(pady=5)

    # add_button = ttk.Button(
    #     room_listbox_frame,
    #     text="Add",
    #     command=lambda: add_building(state, building_treeview, new_room_text),
    # )
    # add_button.pack(side=tk.LEFT, padx=5, pady=5)

    # remove_button = ttk.Button(
    #     room_listbox_frame,
    #     text="Remove",
    #     command=lambda: remove_building(state, building_treeview),
    # )
    # remove_button.pack(side=tk.LEFT, padx=5, pady=5)

    return project_info_tab
