from src.utils.fp_utils import *

import tkinter as tk
from tkinter import ttk

from src.tabs.calc_criteria_tab.utils import save_project_calcType_info
from src.tabs.wm_common_tab.utils import create_tksheet_commonWM, on_select_wmCatCombo
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

    bigArea1 = ttk.Frame(main_paned_window, width=3000, height=1000)

    main_paned_window.add(bigArea1, stretch="always")
    section0 = ttk.Frame(bigArea1, height=70)
    section1 = ttk.Frame(bigArea1, width=3000, height=1000)
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

    ############################################
    wmCat_comboBox_frame = ttk.Frame(section1, width=300, style="Custom.TFrame")
    wmCat_comboBox_frame.pack(anchor="nw")

    wmCat_combo_label = ttk.Label(
        wmCat_comboBox_frame, text="공통항목분류", style="Custom.TLabel"
    )
    wmCat_combo_label.config(cursor="question_arrow")
    wmCat_combo_label.pack(side="left", anchor="w")

    # Define the dropdown values for the headers
    state.wmCat_col_widths = [150, 100, 30, 75, 1300, 100, 100]
    state.wmCat_row_heights = 27

    wmCat_dropdown_values = ["RC공통", "철골공통", "조적공통", "마감공통"]

    wmCat_comboBox = ttk.Combobox(wmCat_comboBox_frame)
    wmCat_comboBox.config(
        values=wmCat_dropdown_values,
        state="readonly",
        height=20,
    )  # 콤보 박스에 사용자가 직접 입력 불가
    wmCat_comboBox.set("공통항목분류를 선택!")  # 맨 처음 나타낼 값 설정
    # calc_comboBox.pack(padx=10, pady=10, anchor="n")
    wmCat_comboBox.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

    wmCat_comboBox.bind(
        "<<ComboboxSelected>>",
        lambda e: on_select_wmCatCombo(
            e,
            state,
        ),
    )
    state.wmCat_comboBox = wmCat_comboBox

    ############################################

    common_wm_data = go(
        collect_level_6_items(state.stdTypes_info, level=0, current_items=None),
        filter(lambda x: "공통|" in x),
        sorted,
        map(lambda x: [x]),
        list,
    )
    state.common_wm_data = common_wm_data

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
        data=[],
        # data=common_wm_data,
        width=3000,
        height=1000,
    )
    state.commonWM_sheet = commonWM_sheet
    commonWM_sheet.pack()
