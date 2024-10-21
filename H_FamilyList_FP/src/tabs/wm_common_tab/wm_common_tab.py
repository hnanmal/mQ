import tkinter as tk
from tkinter import ttk

from src.tabs.calc_criteria_tab.utils import save_project_calcType_info
from src.tabs.wm_common_tab.utils import create_tksheet_commonWM


def create_wm_common_tab(notebook, state, mode=None):
    """Create the '공통 WM 입력' tab with two sections."""
    wm_common_tab = ttk.Frame(notebook)
    if mode == None:
        notebook.add(wm_common_tab, text="공통 WM 입력")
    elif mode == "newWindow_room":
        wm_common_tab.pack(
            side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True
        )

    main_paned_window = tk.PanedWindow(
        wm_common_tab,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    main_paned_window.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    bigArea1 = ttk.Frame(main_paned_window, width=500, height=200)

    main_paned_window.add(bigArea1, stretch="always")
    section0 = ttk.Frame(bigArea1, height=70)
    section1 = ttk.Frame(bigArea1, width=300, height=200)
    section0.pack(side=tk.TOP, anchor="w", fill=tk.X)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.Y, expand=True)

    save_load_btn_frame = ttk.Frame(section0, width=100, relief="ridge")
    save_load_btn_frame.pack(pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="right", padx=10, pady=10)
    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_calcType_info(state),
    )
    save_info_button.pack(side="left", padx=10, pady=10, anchor="w")

    headers = ["wmGrps", "wm"]
    commonWM_sheet = create_tksheet_commonWM(state, section1, headers=headers)
    commonWM_sheet.pack()
