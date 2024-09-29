# src/tabs/familyType_manage_tab/room_tab.py

import json
import tkinter as tk
from tkinter import ttk

from src.tabs.familyType_manage_tab.utils import (
    on_doubleClick_newWindow,
    save_project_roomType_info,
    search_stdTypes,
    update_checkCanvas_data,
)
from src.tabs.familyType_manage_tab.checkListbox import (
    CheckListCanvas,
)


def create_room_tab(notebook, state):
    room_tab = ttk.Frame(notebook)
    notebook.add(room_tab, text="Room")

    bigArea1 = ttk.Frame(room_tab, width=500, height=70, relief="ridge")
    bigArea2 = ttk.Frame(room_tab, width=500, height=1000, relief="ridge")

    bigArea1.pack(padx=10, pady=10, anchor="w", fill=tk.X, expand=True)
    bigArea2.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    section0 = ttk.Frame(bigArea1, width=200, height=70)
    section1 = ttk.Frame(bigArea2, width=700, height=700, relief="ridge")
    section2 = ttk.Frame(bigArea2, width=700, height=700, relief="ridge")
    section3 = ttk.Frame(bigArea2, width=700, height=700, relief="ridge")

    section0.pack(side=tk.TOP, anchor="w")  # , fill=tk.X)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(
        side=tk.RIGHT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True
    )

    # bigArea1 세부 구성
    save_load_btn_frame = ttk.Frame(section0, width=100, height=70, relief="ridge")
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

    def getSelectedItem(event, checkCanvas, data, combobox):
        print(combobox.get())
        state.current_selected_building = combobox.get()
        selected_building = state.current_selected_building
        update_checkCanvas_data(state, checkCanvas, data, selected_building, cat="Room")
        return combobox.get()

    bd_comboBox = ttk.Combobox(section0)
    bd_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가
    bd_comboBox.config(cursor="bottom_side")  # 콤보 박스 마우스 커서
    bd_comboBox.set(" ")  # 맨 처음 나타낼 값 설정
    bd_comboBox.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")
    state.bd_combobox_room = bd_comboBox
    bd_comboBox.bind(
        "<<ComboboxSelected>>",
        lambda e: getSelectedItem(
            e, state.checkCanvas_room, state.project_info, bd_comboBox
        ),
    )
    try:
        print(state.current_selected_building)
    except:
        pass

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
    std_type_label = ttk.Label(
        section1, text="Using Standard Type List", font=("Arial", 14)
    )
    std_type_label.pack(padx=10, pady=10, anchor="w")

    ### Standard Type List 구간

    stdTypes_appliedListbox = tk.Listbox(section1, selectmode=tk.SINGLE, height=20)
    stdTypes_appliedListbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # stdTypes_listbox = tk.Listbox(section1, selectmode=tk.SINGLE, height=20)
    # stdTypes_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Insert std_type data for Room
    # state.section1_room_tab = section1
    # state.checkCanvas_room = CheckListCanvas(state, section1)

    section1.bind(
        "<Double-Button-1>",
        lambda e: on_doubleClick_newWindow(
            e,
            state,
            stdTypes_appliedListbox,
        ),
    )
