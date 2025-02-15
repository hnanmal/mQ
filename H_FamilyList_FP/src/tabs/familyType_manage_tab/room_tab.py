# src/tabs/familyType_manage_tab/room_tab.py

import json
import tkinter as tk
from tkinter import ttk

from src.tabs.familyType_manage_tab.utils import (
    add_room_to_apply_target_rooms,
    add_stdType_roomCat,
    add_to_appliedRoom_data,
    create_assignWMsheet,
    create_tksheet,
    del_stdType_roomCat,
    on_click_stdType_treeItem,
    on_right_click_stdTypetree_roomTab,
    open_calcType_view,
    open_excel_locally,
    remove_from_appliedRoom_data,
    save_project_roomType_info,
    update_selected_calcType,
    update_stdTypeTree_inRoom,
)

from src.tabs.input_common_tab.utils import create_defaultTreeview
from src.views.tooltips import CreateToolTip


def create_room_tab(notebook, state):
    # bgcolorForApply = "#e4dae6"
    # bgcolorForApply = "#EEE5A2"
    bgcolorForApply = "#e8e1ae"
    style = ttk.Style()
    style.configure(
        "Custom.TLabel",
        foreground="blue",
        background=bgcolorForApply,
        font=("Arial", 11),
    )
    style.configure(
        "Custom.TFrame",
        foreground="black",  # Normal text
        background=bgcolorForApply,
    )
    style.map(
        "Custom.TFrame",
        background=[("selected", "lightblue")],  # Background when selected
        highlightcolor=[("selected", "darkblue")],
    )

    style.configure(
        "Custom.Treeview",
        background="white",  # Normal background
        foreground="black",  # Normal text
        fieldbackground="white",  # Entry box background
        bordercolor="blue",  # Border color if needed
        borderwidth=1,
        font=("Arial Narrow", 9),
    )
    style.map(
        "Custom.Treeview",
        # background=[("selected", "lightblue")],  # Background when selected
        background=[("selected", bgcolorForApply)],  # Background when selected
        foreground=[("selected", "blue")],  # Text color when selected
        highlightcolor=[("selected", "darkblue")],
    )

    room_tab = ttk.Frame(notebook)
    notebook.add(room_tab, text="Room")

    state.selected_calcType_name = tk.StringVar()
    state.selected_calcType_name.set("Selected Calc Type:          ")
    state.wmBunches_room = {}
    state.project_info["std_wm_assign"] = {}
    state.selected_building = None
    state.selected_stdType = None
    state.selected_calcType_label = None
    state.selected_calcType_sheetview = None

    WM_col_idx = 4
    unit_col_idx = 2
    wmGrp_col_idx = 0
    desc_col_idx = WM_col_idx + 1
    idxes = [WM_col_idx, unit_col_idx, wmGrp_col_idx, desc_col_idx]
    state.idxes = idxes

    main_paned_window = tk.PanedWindow(
        room_tab,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    main_paned_window.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    bigArea1 = ttk.Frame(main_paned_window, width=500, height=70)
    bigArea2 = ttk.Frame(main_paned_window, width=1200, height=2000)
    bigArea3 = ttk.Frame(main_paned_window, width=700, height=2000)

    bigArea1.pack(padx=10, pady=10, anchor="w", fill=tk.X, expand=True)
    bigArea2.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    bigArea3.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    main_paned_window.add(bigArea1, stretch="always")
    main_paned_window.add(bigArea2, stretch="always")
    main_paned_window.add(bigArea3, stretch="always")

    section0 = ttk.Frame(bigArea1, width=200, height=70)
    section1 = ttk.Frame(bigArea1, width=700, height=2000)
    section2 = ttk.Frame(bigArea2, width=2000, height=2000, relief="groove")
    section3 = ttk.Frame(bigArea3, width=650, height=2000)  # , relief="ridge")

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

    ## 빌딩 콤보박스
    bd_comboBox_frame = ttk.Frame(section2, style="Custom.TFrame")
    bd_comboBox_frame.pack(padx=10, pady=10, anchor="nw")
    bd_combo_label = ttk.Label(
        bd_comboBox_frame, text="1. 작업대상 빌딩 확인", style="Custom.TLabel"
    )
    bd_combo_label.config(cursor="question_arrow")
    bd_combo_label.pack(side="left", padx=10, pady=10, anchor="w")

    bd_comboBox = ttk.Combobox(bd_comboBox_frame)
    bd_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가

    bd_comboBox.set(" ")  # 맨 처음 나타낼 값 설정
    bd_comboBox.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")
    bd_comboLabel_ttp = CreateToolTip(
        bd_combo_label,
        """
>> 레빗 패밀리 타입을 할당할 프로젝트의 건물을 선택하는 곳입니다.
------------------------------
* 할당하려는 레빗 패밀리 타입이 프로젝트의 모든 건물에 공통으로 적용된다면
  '프로젝트 공통'을 선택해 주세요
        """,
    )
    state.bd_combobox_room = bd_comboBox
    ## 바인딩 맨 아래로 위치 이동됨
    # bd_comboBox.bind(
    #     "<<ComboboxSelected>>",
    #     lambda e: update_stdTypeTree_inRoom(e, state, bd_comboBox),
    # )

    ##################################
    ## calc combo box 영역

    calc_comboBox_frame = ttk.Frame(section3, style="Custom.TFrame")
    calc_comboBox_frame.pack(padx=5, pady=5, anchor="nw")

    calc_combo_label = ttk.Label(
        calc_comboBox_frame, text="3. 산출 타입 확인", style="Custom.TLabel"
    )
    calc_combo_label.config(cursor="question_arrow")
    calc_combo_label.pack(side="left", padx=10, pady=10, anchor="w")

    calc_comboBox = ttk.Combobox(calc_comboBox_frame)
    calc_comboBox.config(
        state="readonly", height=20
    )  # 콤보 박스에 사용자가 직접 입력 불가
    calc_comboBox.set("산출 타입 선택")  # 맨 처음 나타낼 값 설정
    # calc_comboBox.pack(padx=10, pady=10, anchor="n")
    calc_comboBox.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")
    calc_comboLabel_ttp = CreateToolTip(
        calc_combo_label,
        """
>> 현재 카테고리에서 지정 가능한 산출 타입을 선택하는 드롭다운 메뉴입니다.
------------------------------
* !! Revit 타입을 스탠다드 항목에 할당할때, 반드시 산출 타입을 확인해 주세요 !!
        """,
    )
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
        section1,
        text="2. 스탠다드 타입 확인\n(Room Finish)",
        font=("Arial", 12),
        style="Custom.TLabel",
    )
    std_type_label.config(cursor="question_arrow")
    std_type_label.pack(padx=10, pady=10, anchor="w")

    std_type_label_ttp = CreateToolTip(
        std_type_label,
        """
>> 더블 클릭하시면 'BIM 팀표준설계정보' 엑셀파일(Interior Finish Style)을 Edge브라우저로 실행합니다
------------------------------

* 룸 카테고리 스탠다드 아이템들을 선택하면 우측 영역에서 각 타입별 WM 을 할당할 수 있습니다.
Floor, Skirt, Wall, Ceiling 으로 구분되어 있습니다.
        """,
    )

    std_type_label.bind(
        "<Double-Button-1>",
        open_excel_locally,
    )

    ### Standard Type Treeview 구간
    stdTypes_treeview = create_defaultTreeview(
        state,
        section1,
        ["stdTypes", "building_tag"],
        height=10,
    )
    stdTypes_treeview.config(
        style="Custom.Treeview",
        selectmode="browse",
    )
    stdTypes_treeview.column("stdTypes", width=200)
    state.stdTypeTree_inRoom = stdTypes_treeview

    stdTypes_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: on_click_stdType_treeItem(
            e, state, stdTypes_treeview, selected_stdType_label
        ),
    )
    stdTypes_treeview.bind(
        "<Button-3>",
        lambda event: on_right_click_stdTypetree_roomTab(
            event, state, stdTypes_treeview
        ),
    )

    new_stdType_text = tk.Text(section1, height=2, width=30)
    new_stdType_text.pack(pady=5, anchor="w")

    add_del_btn_frame = ttk.Frame(section1, width=200, height=70)
    add_del_btn_frame.pack(anchor="w")
    add_stdType_btn = ttk.Button(
        add_del_btn_frame,
        text="Add stdType",
        command=lambda: add_stdType_roomCat(state, new_stdType_text),
    )
    add_stdType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

    del_stdType_btn = ttk.Button(
        add_del_btn_frame,
        text="Del stdType",
        command=lambda: del_stdType_roomCat(state),
    )
    del_stdType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

    ## section2 세부 구성
    common_width = 2000
    common_height = 160
    common_headers = [
        "물량산출식",
        # "Qty",
        "Unit",
        "Gauge Code",
        "WM",
        "Description",
        "Remark",
    ]
    state.common_headers = ["wmGrp"] + common_headers
    state.common_widths = [125, 95, 30, 30, 800, 170, 100]
    state.selected_stdType_name = tk.StringVar()
    state.selected_stdType_name.set("Selected Standard Type: ")
    selected_stdType_label = ttk.Label(
        section2, textvariable=state.selected_stdType_name, font=("Arial", 12)
    )
    selected_stdType_label.config(cursor="question_arrow")
    selected_stdType_label.pack(padx=10, anchor="w")
    selected_stdType_label_ttp = CreateToolTip(
        selected_stdType_label,
        """
>> 좌측에서 선택된 스탠다드 타입에 할당할 WM 를 지정할 수 있습니다.
------------------------------
* WM 항목을 추가하려면 시트 영역에서 우측 버튼을 클릭하여 'insert row' 메뉴를 클릭하십시오.
* 우측의 Selected Calc Type 정보를 참조하여 물량산출식 열을 채워 주십시오.
------------------------------
* 기존 저장된 항목을 수정하려면 셀을 더블 클릭하여 편집하면 됩니다.
* 현재 상태를 저장하려면 좌측 최상단의 'Save Project Info' 버튼을 누르십시오.
        """,
    )

    #########stdType_wm_label#####################
    stdType_wm_label = ttk.Label(section2, text="Standard Type's WorkMaster")
    stdType_wm_label.pack(padx=10, pady=10, anchor="w")
    ##############################################

    floor_dropdowns = list(filter(lambda x: "바닥" in x, state.wm_group_data))
    state.floor_dropdowns = floor_dropdowns
    assignWM_sheetview_forStdType_forFloor = create_assignWMsheet(
        state,
        section2,
        ["Floor"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=floor_dropdowns,
    )
    assignWM_sheetview_forStdType_forFloor.pack(padx=5, pady=2, anchor="w")
    state.assignWM_sheetview_forStdType_forFloor = (
        assignWM_sheetview_forStdType_forFloor
    )

    base_dropdowns = list(filter(lambda x: "걸레받이" in x, state.wm_group_data))
    state.base_dropdowns = base_dropdowns
    assignWM_sheetview_forStdType_forBase = create_assignWMsheet(
        state,
        section2,
        ["Base"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=base_dropdowns,
    )
    assignWM_sheetview_forStdType_forBase.pack(padx=5, pady=2, anchor="w")
    state.assignWM_sheetview_forStdType_forBase = assignWM_sheetview_forStdType_forBase

    wall_dropdowns = list(filter(lambda x: "벽" in x, state.wm_group_data))
    state.wall_dropdowns = wall_dropdowns
    assignWM_sheetview_forStdType_forWall = create_assignWMsheet(
        state,
        section2,
        ["Wall"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=wall_dropdowns,
    )
    assignWM_sheetview_forStdType_forWall.pack(padx=5, pady=2, anchor="w")
    state.assignWM_sheetview_forStdType_forWall = assignWM_sheetview_forStdType_forWall

    ceil_dropdowns = list(filter(lambda x: "천장" in x, state.wm_group_data))
    state.ceil_dropdowns = ceil_dropdowns
    assignWM_sheetview_forStdType_forCeiling = create_assignWMsheet(
        state,
        section2,
        ["Ceiling"] + common_headers,
        height=common_height,
        width=common_width,
        dropdowns=ceil_dropdowns,
    )
    assignWM_sheetview_forStdType_forCeiling.pack(padx=5, pady=2, anchor="w")
    state.assignWM_sheetview_forStdType_forCeiling = (
        assignWM_sheetview_forStdType_forCeiling
    )

    selected_calcType_label = ttk.Label(
        section3, textvariable=state.selected_calcType_name, font=("Arial", 11)
    )
    selected_calcType_label.config(cursor="question_arrow")
    selected_calcType_label.pack(padx=10, pady=10, anchor="w")
    state.selected_calcType_label = selected_calcType_label
    selected_calcType_label_ttp = CreateToolTip(
        selected_calcType_label,
        """
>> 위에서 선택된 산출 타입에 대한 수식 약자들이 참조용으로 제공됩니다.
------------------------------
* 항목과 수식약자 열을 참조하여 WM 항목 별 물량산출식을 작성해 주세요.
* 더블 클릭하면 별도의 새 창으로 산출 타입을 조회 할 수 있습니다.
  (새 창에서는 산출타입 내용 편집 가능)
------------------------------
* !! Revit 타입을 스탠다드 항목에 할당할때, 반드시 산출 타입을 확인해 주세요 !!
        """,
    )
    selected_calcType_label.bind(
        "<Double-Button-1>",
        lambda e: open_calcType_view(e, state),
    )

    selected_calcType_sheetview = create_tksheet(
        state,
        section3,
        ["항목", "수식약자", "적용값"],
        width=700,
        height=150,
        mode="calcType",
    )
    selected_calcType_sheetview.pack(padx=10, pady=10, anchor="w")
    state.selected_calcType_sheetview = selected_calcType_sheetview

    apply_frame = ttk.Frame(section3, style="Custom.TFrame")
    apply_frame.pack(padx=5, pady=5, anchor="w")

    applied_famType_label = ttk.Label(
        apply_frame,
        text="4. 레빗 패밀리 할당 현황",
        font=("Arial", 11, "bold"),
        style="Custom.TLabel",
    )
    applied_famType_label.config(cursor="question_arrow")
    applied_famType_label.pack(padx=10, pady=10, anchor="w")

    applied_famType_label_ttp = CreateToolTip(
        applied_famType_label,
        """
>> 현재 선택된 Standard Type에 산출WM항목을 연결할 레빗패밀리를 등록하는 구역입니다.

* 신규 룸을 추가하고 싶으면 아래의 Not Applied 영역에서 우측 버튼>insert row 를 통해
  새로운 룸의 번호와 이름을 기입하고, [↑] 버튼을 눌러주시면 Applied 영역에 추가 됩니다.
        """,
    )

    applied_famType_sheetview = create_tksheet(
        state,
        apply_frame,
        ["no", "rooms", "stdType_tag", "bd_tag", "calc_tag"],
        width=700,
        height=200,
    )
    applied_famType_sheetview.pack(padx=10, pady=10, anchor="w")
    state.applied_famType_sheetview = applied_famType_sheetview

    add_del_famType_btn_frame = ttk.Frame(
        apply_frame, width=200, height=70, style="Custom.TFrame"
    )
    add_del_famType_btn_frame.pack(padx=10, pady=10, anchor="w")
    add_famType_btn = ttk.Button(
        add_del_famType_btn_frame,
        text="↑",
        command=lambda: add_to_appliedRoom_data(state),
    )
    add_famType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

    del_stdType_btn = ttk.Button(
        add_del_famType_btn_frame,
        text="↓",
        command=lambda: remove_from_appliedRoom_data(state),
    )
    del_stdType_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="e")

    notApplied_famType_label = ttk.Label(
        apply_frame,
        text="Not Applied Revit Family Types",
        font=("Arial", 11),
        style="Custom.TLabel",
    )
    notApplied_famType_label.pack(padx=10, pady=10, anchor="w")
    notApplied_famType_label.config(cursor="question_arrow")
    notApplied_famType_label_ttp = CreateToolTip(
        notApplied_famType_label,
        """
>> 'Project Standard > 프로젝트 정보 입력' 탭에서 입력한 Room 중, 아직 Std 할당이 이루어지지 않은 룸들의 목록입니다.
------------------------------
* 현재 선택된 std 항목으로 할당하려면 ↑ 버튼을 클릭하세요.
* 'Project Standard > 프로젝트 정보 입력'에서 입력하지 않은 룸을 임의로 추가하려면 '우측버튼 > insert row' 후에 'no'와 'rooms' 항목을 작성한뒤 ↑ 버튼을 클릭하세요.
        """,
    )

    notApplied_famType_sheetview = create_tksheet(
        state,
        apply_frame,
        ["no", "rooms", "stdType_tag", "bd_tag"],
        width=700,
        height=150,
        mode="nonAppFamtype",
    )
    notApplied_famType_sheetview.pack(padx=10, pady=10, anchor="w")
    state.notApplied_famType_sheetview = notApplied_famType_sheetview
    notApplied_famType_sheetview.extra_bindings(
        [
            (
                "end_edit_cell",
                # lambda e: update_second_cell_dropdown(e, state, sheet),
                lambda e: add_room_to_apply_target_rooms(
                    e, state, notApplied_famType_sheetview
                ),
            ),
        ]
    )
    notApplied_famType_sheetview.set_options(header_bg="#ededed")
    notApplied_famType_sheetview.set_options(index_bg="#ededed")
    notApplied_famType_sheetview.set_options(table_bg="#f7f7f7")

    bd_comboBox.bind(
        "<<ComboboxSelected>>",
        lambda e: update_stdTypeTree_inRoom(e, state, bd_comboBox),
    )
