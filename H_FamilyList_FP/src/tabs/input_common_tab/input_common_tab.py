# src/tabs/input_common_tab/input_common_tab.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

from src.tabs.project_info_tab.common_utils import save_project_info


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

    # state.logging_text_widget.write(str(state.current_loaded_pjt))

    # def on_file_path_change(*args):
    #     print(f"File path changed to: {file_load_status}")

    # file_load_status = state["current_loaded_pjt"].get()
    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="top", padx=10, pady=10)

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_info(
            # state,
            # project_name_var,
            # project_type_var,
            # building_treeview,
            # room_treeview,
        ),
    )
    save_info_button.pack(side="left", padx=30, pady=10, anchor="w")
