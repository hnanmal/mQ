# src/tabs/input_common_tab/input_common_tab.py
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


def create_input_common_tab(notebook, state):
    """Create the '공통 정보 입력' tab with two sections."""
    input_common_tab = ttk.Frame(notebook)
    notebook.add(input_common_tab, text="공통 정보 입력")

    # Divide the tab into three sections (frames)
    section0 = ttk.Frame(input_common_tab, height=70)
    section1 = ttk.Frame(input_common_tab, width=300, height=200)
    section2 = ttk.Frame(input_common_tab, width=400, height=200)

    section0.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    save_load_btn_frame = ttk.Frame(section0, width=300)
    save_load_btn_frame.pack(pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="right", padx=10, pady=10)

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_common_info(
            state,
            earth_treeview,
            steel_treeview,
        ),
    )
    save_info_button.pack(side="left", padx=30, pady=10, anchor="w")

    earth_label = ttk.Label(section1, text="Earth Work", font=("Arial", 14))
    earth_label.pack(pady=10, anchor="w")

    steel_label = ttk.Label(section2, text="Steel Work", font=("Arial", 14))
    steel_label.pack(pady=10, anchor="w")

    earth_tree_frame = ttk.Frame(section1, width=200)
    earth_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    earth_treeview = create_defaultTreeview(
        state,
        earth_tree_frame,
        ("항목", "입력값", "단위", "비고"),
    )
    state.earth_treeview = earth_treeview

    new_earthParam_text = tk.Text(section1, height=4, width=30)
    new_earthParam_text.pack(pady=5, anchor="w")

    add_common_earthParam_button = ttk.Button(
        section1,
        text="Add",
        command=lambda: add_common_param(state, earth_treeview, new_earthParam_text),
    )
    add_common_earthParam_button.pack(side=tk.LEFT, padx=5, pady=5)

    steel_tree_frame = ttk.Frame(section2, width=200)
    steel_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    steel_treeview = create_defaultTreeview(
        state,
        steel_tree_frame,
        ("항목", "입력값", "단위", "비고"),
    )
    state.steel_treeview = steel_treeview

    new_steelParam_text = tk.Text(section2, height=4, width=30)
    new_steelParam_text.pack(pady=5, anchor="w")

    add_common_steelParam_button = ttk.Button(
        section2,
        text="Add",
        command=lambda: add_common_param(state, steel_treeview, new_steelParam_text),
    )
    add_common_steelParam_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Bind refresh when tab is clicked or focus changes
    def update_tab_content(event):
        refresh_treeview(earth_treeview, state.project_info, "earth")
        refresh_treeview(steel_treeview, state.project_info, "steel")

    input_common_tab.bind("<Visibility>", update_tab_content)
