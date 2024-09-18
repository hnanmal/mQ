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


def create_input_common_tab(notebook, state):
    """Create the '공통 정보 입력' tab with two sections."""
    input_common_tab = ttk.Frame(notebook)
    notebook.add(input_common_tab, text="공통 정보 입력")

    # Divide the tab into three sections (frames)
    section0 = ttk.Frame(input_common_tab, height=70)
    section1 = ttk.Frame(input_common_tab, width=300, height=200)
    section2 = ttk.Frame(input_common_tab, width=400, height=200)

    section0.pack(side=tk.TOP, fill=tk.BOTH)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    save_load_btn_frame = ttk.Frame(section0, width=300)
    save_load_btn_frame.pack(pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="top", padx=10, pady=10)

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
    earth_default_items = [
        ("Lean 두께", 0.1, "M", ""),
        ("Base 두께", 0.15, "M", ""),
        ("SubBase 두께", 0.15, "M", ""),
        ("ExtraExcavation 두께", 0.1, "M", ""),
        ("토량환산계수", 1.15, "", ""),
        ("터파기 여유폭", 0.2, "M", ""),
        ("지하수위", -1, "M", "GL 을 기준으로 음수로 작성"),
    ]
    # Insert some sample data into the tree
    for item in earth_default_items:
        if item not in state.project_info["common_info"]["earth"]:
            earth_treeview.insert("", "end", values=item)

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

    steel_default_items = [
        ("Extra Heavy Steel", 200, "KG/M", ""),
        ("Heavy Steel", 90, "KG/M", ""),
        ("Medium Steel", "", "KG/M", "입력 불필요"),
        ("Light Steel", 30, "KG/M", ""),
        ("Extra Light Steel", 10, "KG/M", ""),
    ]
    # Insert some sample data into the tree
    for item in steel_default_items:
        if item not in state.project_info["common_info"]["steel"]:
            steel_treeview.insert("", "end", values=item)

    new_steelParam_text = tk.Text(section2, height=4, width=30)
    new_steelParam_text.pack(pady=5, anchor="w")

    add_common_steelParam_button = ttk.Button(
        section2,
        text="Add",
        command=lambda: add_common_param(state, steel_treeview, new_steelParam_text),
    )
    add_common_steelParam_button.pack(side=tk.LEFT, padx=5, pady=5)
