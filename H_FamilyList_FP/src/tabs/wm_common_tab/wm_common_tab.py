import tkinter as tk
from tkinter import ttk

from src.tabs.calc_criteria_tab.utils import save_project_calcType_info
from src.tabs.wm_common_tab.utils import create_tksheet_commonWM
from src.views.listbox_utils import collect_level_6_items


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

    bigArea1 = ttk.Frame(main_paned_window, width=1500, height=1000)

    main_paned_window.add(bigArea1, stretch="always")
    section0 = ttk.Frame(bigArea1, height=70)
    section1 = ttk.Frame(bigArea1, width=1500, height=1000)
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

    common_data = list(
        map(
            lambda x: [x],
            filter(
                lambda x: "공통|" in x,
                collect_level_6_items(state.stdTypes_info, level=0, current_items=None),
            ),
        )
    )

    common_headers = [
        "wmGrp",
        "물량산출식",
        "Unit",
        "Gauge Code",
        "WM",
        "Description",
        "Remark",
    ]
    commonWM_sheet = create_tksheet_commonWM(
        state,
        section1,
        headers=common_headers,
        data=common_data,
        width=1500,
        height=1000,
    )
    commonWM_sheet.pack()
