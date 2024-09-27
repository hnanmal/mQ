# src/tabs/familyType_manage_tab/room_tab.py

import json
import tkinter as tk
from tkinter import ttk

from src.tabs.familyType_manage_tab.utils import (
    save_project_roomType_info,
    search_stdTypes,
)
from src.tabs.familyType_manage_tab.checkListbox import (
    CheckListCanvas,
)


def create_room_tab(notebook, state):
    room_tab = ttk.Frame(notebook)
    notebook.add(room_tab, text="Room")

    bigArea1 = ttk.Frame(room_tab, width=500, height=70)
    bigArea2 = ttk.Frame(room_tab)

    bigArea1.pack(side=tk.TOP, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    bigArea2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    section0 = ttk.Frame(bigArea1, width=500, height=70)
    section1 = ttk.Frame(bigArea2, width=500, height=200, relief="ridge")
    section2 = ttk.Frame(bigArea2, width=500, height=200)
    section3 = ttk.Frame(bigArea2, width=500, height=200)

    section0.pack(side=tk.TOP, anchor="w", fill=tk.X)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    # bigArea1 세부 구성
    save_load_btn_frame = ttk.Frame(section0, width=100, relief="ridge")
    save_load_btn_frame.pack(side="left", pady=10, anchor="w")

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_roomType_info(state),
    )
    save_info_button.pack(side="left", padx=10, pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="left", padx=10, pady=10)

    bd_comboBox = ttk.Combobox(section0)
    bd_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가
    bd_comboBox.config(cursor="bottom_side")  # 콤보 박스 마우스 커서
    bd_comboBox.set("대상 빌딩 선택")  # 맨 처음 나타낼 값 설정
    bd_comboBox.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")
    state.bd_combobox_room = bd_comboBox

    calc_comboBox = ttk.Combobox(section0)
    calc_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가
    calc_comboBox.config(cursor="bottom_side")  # 콤보 박스 마우스 커서
    calc_comboBox.set("산출 타입 선택")  # 맨 처음 나타낼 값 설정
    calc_comboBox.pack(side=tk.RIGHT, padx=10, pady=10, anchor="e")
    state.calc_comboBox_room = calc_comboBox

    # bigArea2 세부 구성
    ## section1 세부 구성
    std_type_label = ttk.Label(section1, text="Standard Type List", font=("Arial", 14))
    std_type_label.pack(padx=10, pady=10, anchor="w")

    ### search 영역
    search_var = tk.StringVar()
    search_entry = ttk.Entry(section1, textvariable=search_var)
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

    ### Standard Type List 구간

    # stdTypes_listbox = tk.Listbox(section1, selectmode=tk.SINGLE, height=20)
    # stdTypes_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Insert std_type data for Room

    state.checkCanvas_room = CheckListCanvas(section1)
