# src/tabs/familyType_manage_tab/room_tab.py

import json
import tkinter as tk
from tkinter import ttk

from src.tabs.familyType_manage_tab.utils import (
    create_assignWMsheet,
    create_tksheet,
    save_project_roomType_info,
    search_stdTypes,
    update_second_cell_dropdown,
    update_selected_calcType,
    update_selected_stdType_label_inRoom,
    update_stdTypeTree_inRoom,
)
from src.tabs.familyType_manage_tab.checkListbox import (
    CheckListCanvas,
)
from src.tabs.input_common_tab.utils import create_defaultTreeview


def create_room_tab(notebook, state):
    room_tab = ttk.Frame(notebook)
    notebook.add(room_tab, text="Room")
    state.selected_calcType_name = tk.StringVar()
    state.selected_calcType_name.set("Selected Calc Type:          ")

    bigArea1 = ttk.Frame(room_tab, width=500, height=70)
    bigArea2 = ttk.Frame(room_tab, width=1200, height=2000, relief="ridge")

    bigArea1.pack(padx=10, pady=10, anchor="w", fill=tk.X, expand=True)
    bigArea2.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    section0 = ttk.Frame(bigArea1, width=200, height=70)
    section1 = ttk.Frame(bigArea2, width=700, height=2000)
    section2 = ttk.Frame(bigArea2, width=1200, height=2000, relief="ridge")
    section3 = ttk.Frame(bigArea2, width=500, height=2000, relief="ridge")

    section0.pack(side=tk.TOP, anchor="w")  # , fill=tk.X)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

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

    bd_comboBox = ttk.Combobox(section0)
    bd_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가
    bd_comboBox.config(cursor="bottom_side")  # 콤보 박스 마우스 커서
    bd_comboBox.set(" ")  # 맨 처음 나타낼 값 설정
    bd_comboBox.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")
    state.bd_combobox_room = bd_comboBox
    # bd_comboBox.bind(
    #     "<<ComboboxSelected>>",
    #     lambda e: update_stdTypeTree_inRoom(e, state, bd_comboBox),
    # )

    apply_typeToBuilding_btn = ttk.Button(
        section0,
        text="현재 선택 타입을 상기 빌딩에 적용하기",
        command=lambda: apply_typeToBuilding(state),
    )
    apply_typeToBuilding_btn.pack(side="left", padx=10, pady=10)

    calc_comboBox = ttk.Combobox(section3)
    calc_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가
    calc_comboBox.config(cursor="bottom_side")  # 콤보 박스 마우스 커서
    calc_comboBox.set("산출 타입 선택")  # 맨 처음 나타낼 값 설정
    calc_comboBox.pack(padx=10, pady=10, anchor="n")
    calc_comboBox.bind(
        "<<ComboboxSelected>>",
        lambda e: update_selected_calcType(
            e,
            state,
            calc_comboBox,
            selected_calcType_label,
            selected_calcType_sheetview,
        ),
    )
    state.calc_comboBox_room = calc_comboBox

    # bigArea2 세부 구성
    ## section1 세부 구성
    std_type_label = ttk.Label(
        section1, text="Using Standard Type List", font=("Arial", 14)
    )
    std_type_label.pack(padx=10, pady=10, anchor="w")

    ### Standard Type Treeview 구간
    stdTypes_treeview = create_defaultTreeview(
        state, section1, ["stdTypes", "building_tag"], height=15
    )
    state.stdTypeTree_inRoom = stdTypes_treeview

    stdTypes_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: update_selected_stdType_label_inRoom(
            e, state, stdTypes_treeview, selected_stdType_label
        ),
    )
    add_del_btn_frame = ttk.Frame(section1, width=200, height=70)
    add_del_btn_frame.pack(padx=10, pady=10, anchor="w")
    add_stdType_btn = ttk.Button(
        add_del_btn_frame,
        text="add stdType",
        command=lambda: add_stdType_roomCat(state),
    )
    add_stdType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

    del_stdType_btn = ttk.Button(
        add_del_btn_frame,
        text="del stdType",
        command=lambda: del_stdType_roomCat(state),
    )
    del_stdType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

    ## section2 세부 구성
    common_width = 1200
    common_height = 140
    common_headers = [
        "물량산출식",
        "Qty",
        "Unit",
        "WM",
        "Gauge Code",
        "Description",
        "Remark",
    ]
    state.selected_stdType_name = tk.StringVar()
    state.selected_stdType_name.set("Selected Standard Type: ")
    selected_stdType_label = ttk.Label(
        section2, textvariable=state.selected_stdType_name, font=("Arial", 12)
    )
    selected_stdType_label.pack(padx=10, pady=10, anchor="w")

    floor_dropdowns = list(filter(lambda x: "바닥" in x, state.wm_group_data))
    assignWM_sheetview_forStdType_forFloor = create_assignWMsheet(
        state,
        section2,
        ["Floor"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=floor_dropdowns,
    )
    assignWM_sheetview_forStdType_forFloor.pack(padx=5, pady=2, anchor="w")

    base_dropdowns = list(filter(lambda x: "걸레받이" in x, state.wm_group_data))
    assignWM_sheetview_forStdType_forBase = create_assignWMsheet(
        state,
        section2,
        ["Base"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=base_dropdowns,
    )
    assignWM_sheetview_forStdType_forBase.pack(padx=5, pady=2, anchor="w")

    wall_dropdowns = list(filter(lambda x: "벽" in x, state.wm_group_data))
    assignWM_sheetview_forStdType_forWall = create_assignWMsheet(
        state,
        section2,
        ["Wall"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=wall_dropdowns,
    )
    assignWM_sheetview_forStdType_forWall.pack(padx=5, pady=2, anchor="w")

    ceil_dropdowns = list(filter(lambda x: "천장" in x, state.wm_group_data))
    assignWM_sheetview_forStdType_forCeiling = create_assignWMsheet(
        state,
        section2,
        ["Ceiling"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=ceil_dropdowns,
    )
    assignWM_sheetview_forStdType_forCeiling.pack(padx=5, pady=2, anchor="w")

    selected_calcType_label = ttk.Label(
        section3, textvariable=state.selected_calcType_name, font=("Arial", 11)
    )
    selected_calcType_label.pack(padx=10, pady=10, anchor="w")

    selected_calcType_sheetview = create_tksheet(
        state,
        section3,
        ["항목", "수식약자", "적용값"],
        height=150,
        mode="calcType",
    )
    selected_calcType_sheetview.pack(padx=10, pady=10, anchor="w")

    applied_famType_label = ttk.Label(
        section3, text="Applied Revit Family Types", font=("Arial", 11)
    )
    applied_famType_label.pack(padx=10, pady=10, anchor="w")

    applied_famType_sheetview = create_tksheet(
        state,
        section3,
        ["famType", "bd_tag", "calc_tag"],
        height=150,
    )
    applied_famType_sheetview.pack(padx=10, pady=10, anchor="w")

    add_del_famType_btn_frame = ttk.Frame(section3, width=200, height=70)
    add_del_famType_btn_frame.pack(padx=10, pady=10, anchor="w")
    add_famType_btn = ttk.Button(
        add_del_famType_btn_frame,
        text="↑",
        command=lambda: add_famType_roomCat(state),
    )
    add_famType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

    del_stdType_btn = ttk.Button(
        add_del_famType_btn_frame,
        text="↓",
        command=lambda: del_famType_roomCat(state),
    )
    del_stdType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="e")

    notApplied_famType_label = ttk.Label(
        section3, text="Not Applied Revit Family Types", font=("Arial", 11)
    )
    notApplied_famType_label.pack(padx=10, pady=10, anchor="w")

    notApplied_famType_sheetview = create_tksheet(
        state,
        section3,
        ["famType"],
        height=150,
        mode="nonAppFamtype",
    )
    notApplied_famType_sheetview.pack(padx=10, pady=10, anchor="w")
    state.notApplied_famType_sheetview = notApplied_famType_sheetview

    bd_comboBox.bind(
        "<<ComboboxSelected>>",
        lambda e: update_stdTypeTree_inRoom(e, state, bd_comboBox),
    )
