# src/tabs/familyType_manage_tab/room_tab.py

import json
import tkinter as tk
from tkinter import ttk

from src.tabs.familyType_manage_tab.utils import (
    creat_combo_buildingList,
    save_project_roomType_info,
)


def create_room_tab(notebook, state):
    room_tab = ttk.Frame(notebook)
    notebook.add(room_tab, text="Room")

    bigArea1 = ttk.Frame(room_tab, width=500, height=70)
    bigArea2 = ttk.Frame(room_tab)

    bigArea1.pack(side=tk.TOP, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    bigArea2.pack(
        side=tk.BOTTOM, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True
    )

    section0 = ttk.Frame(bigArea1, width=500, height=70)
    section1 = ttk.Frame(bigArea2, width=500, height=200)
    section2 = ttk.Frame(bigArea2, width=500, height=200)
    section3 = ttk.Frame(bigArea2, width=500, height=200)

    section0.pack(side=tk.TOP, anchor="w", fill=tk.X)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    # bigArea1 세부 구성
    save_load_btn_frame = ttk.Frame(section0, width=100)
    save_load_btn_frame.pack(pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="right", padx=10, pady=10)

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_roomType_info(state),
    )
    save_info_button.pack(side="left", padx=10, pady=10, anchor="w")

    state.project_info_var = tk.StringVar()
    try:
        building_list = json.dump(state.project_info_var.get())
        combo_box = ttk.Combobox(section0, textvariable=building_list)
        combo_box.pack(pady=20)
    except:
        pass

    # bigArea2 세부 구성
    ## section1 세부 구성
