# src/tabs/calc_criteria_tab/calc_criteria_tab.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

# from src.tabs.project_info_tab.common_utils import save_project_info
from src.tabs.input_common_tab.utils import (
    add_common_param,
    create_defaultTreeview,
    save_project_common_info,
)
from src.tabs.project_info_tab.common_utils import refresh_treeview


def create_calc_criteria_tab(notebook, state):
    """Create the '공통 정보 입력' tab with two sections."""
    input_common_tab = ttk.Frame(notebook)
    notebook.add(input_common_tab, text="산출 기준")

    # Divide the tab into three sections (frames)
    section0 = ttk.Frame(input_common_tab, height=70)
    section1 = ttk.Frame(input_common_tab, width=150, height=200)
    section2 = ttk.Frame(input_common_tab, width=500, height=200)
    section3 = ttk.Frame(input_common_tab, width=300, height=200)

    section0.pack(side=tk.TOP, fill=tk.BOTH)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    save_load_btn_frame = ttk.Frame(section0, width=300)
    save_load_btn_frame.pack(pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="top", padx=10, pady=10)

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_calc_criteria(
            state,
            earth_treeview,
            steel_treeview,
        ),
    )
    save_info_button.pack(side="left", padx=30, pady=10, anchor="w")

    # Category List Title
    category_list_label = ttk.Label(section1, text="Category List", font=("Arial", 14))
    category_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar
    cat_treeview_frame = ttk.Frame(section1, width=300)
    cat_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    cat_treeview = ttk.Treeview(
        cat_treeview_frame,
        columns=("Category Name",),
        show="headings",
        height=8,
    )

    cat_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    cat_treeview.heading("Category Name", text="Category Name")

    scrollbar = ttk.Scrollbar(
        cat_treeview_frame, orient=tk.VERTICAL, command=cat_treeview.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    cat_treeview.config(yscrollcommand=scrollbar.set)

    default_cat_list = [
        "Room",
        "Floors",
        "Roofs",
        "Walls",
        "St_Fdn",
        "St_Col",
        "St_Framing",
        "Ceilings",
        "Doors",
        "Windows",
        "Stairs",
        "Railings",
        "Generic",
    ]

    for i in default_cat_list:
        cat_treeview.insert(
            "",
            "end",
            values=(i),
        )

    # Section 2 - Selected Category's Criteria list
    selected_Cat_label = ttk.Label(
        section2, text="Selected Category: ", font=("Arial", 14)
    )
    selected_Cat_label.pack(pady=10, anchor="w")
