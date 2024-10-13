import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

from src.tabs.project_info_tab.bd_treeview_utils import (
    add_building,
    auto_numbering,
    on_building_select,
    on_click_edit,
    remove_building,
)
from src.tabs.project_info_tab.common_utils import (
    load_project_info,
    save_project_info,
)
from src.views.treeview_handlers import create_treeview_forPjinfo
from src.tabs.project_info_tab.room_treeview_utils import (
    add_item_in_roomTree,
    remove_item_in_roomTree,
)
from src.views.tooltips import CreateToolTip


def create_project_info_tab(notebook, state):
    """Create the '프로젝트 정보 입력' tab with two sections."""
    project_info_tab = ttk.Frame(notebook)
    notebook.add(project_info_tab, text="프로젝트 정보 입력")
    state.current_loaded_pjt = None
    state.project_info = {
        "project_name": None,
        "project_type": None,
        "common_info": {"earth": [], "steel": []},
        "building_list": [],
    }

    # Divide the tab into three sections (frames)
    section0 = ttk.Frame(project_info_tab, height=70)
    section1 = ttk.Frame(project_info_tab, width=300, height=200)
    section2 = ttk.Frame(project_info_tab, width=400, height=200)
    section3 = ttk.Frame(project_info_tab, width=100, height=200)

    section0.pack(side=tk.TOP, fill=tk.BOTH)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # section0.pack_propagate(False)
    # section1.pack_propagate(False)
    # section2.pack_propagate(False)
    # section3.pack_propagate(False)

    save_load_btn_frame = ttk.Frame(section0, width=300)
    save_load_btn_frame.pack(pady=10, anchor="w")

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_info(
            state,
            project_name_var,
            project_type_var,
        ),
    )
    save_info_button.pack(side="left", padx=20, pady=20, anchor="w")

    load_info_button = ttk.Button(
        save_load_btn_frame,
        text="Load Project Info",
        command=lambda: load_project_info(
            state,
            project_name_var,
            project_type_var,
            building_treeview,
            state.earth_treeview,
            state.steel_treeview,
        ),
    )
    load_info_button.pack(side="left", padx=30, pady=10, anchor="w")

    # Section 1 - Project Info
    project_name_label = ttk.Label(section1, text="Project Name", font=("Arial", 14))
    project_name_label.pack(pady=10, anchor="w")

    project_name_var = tk.StringVar()
    state.project_name_var = project_name_var  ## state 전달
    project_name_entry = ttk.Entry(section1, textvariable=project_name_var, width=30)
    project_name_entry.pack(pady=10, anchor="w")

    # Project Type Label and Dropdown
    project_type_label = ttk.Label(section1, text="Project Type", font=("Arial", 14))
    project_type_label.pack(pady=10, anchor="w")

    project_type_var = tk.StringVar()
    # state.project_type_var = project_type_var  ## state 전달
    project_type_dropdown = ttk.Combobox(
        section1, textvariable=project_type_var, values=["Execution", "Bid"]
    )
    project_type_dropdown.pack(pady=10, anchor="w")

    # Building List Title
    building_list_label = ttk.Label(section1, text="Building List", font=("Arial", 14))
    building_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar
    bd_treeview_frame = ttk.Frame(section1, width=300)
    bd_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    auto_number_button = ttk.Button(
        bd_treeview_frame,
        text="Auto Numbering",
        command=lambda: auto_numbering(state, building_treeview),
    )
    auto_number_button.pack(side=tk.TOP, padx=5, pady=5, anchor="e")

    building_treeview = ttk.Treeview(
        bd_treeview_frame,
        columns=("Building Name", "Number"),
        show="headings",
        height=8,
    )
    # state.building_treeview = building_treeview  ## state 전달

    building_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    building_treeview.heading("Building Name", text="Building Name")
    building_treeview.heading("Number", text="Number")

    building_treeview.column("Building Name", width=150)
    building_treeview.column("Number", width=100)

    scrollbar = ttk.Scrollbar(
        bd_treeview_frame, orient=tk.VERTICAL, command=building_treeview.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    building_treeview.config(yscrollcommand=scrollbar.set)
    state.building_treeview = building_treeview

    new_building_text = tk.Text(section1, height=4, width=30)
    new_building_text.pack(pady=5, anchor="w")

    add_button = ttk.Button(
        section1,
        text="Add",
        command=lambda: add_building(state, building_treeview, new_building_text),
    )
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    remove_button = ttk.Button(
        section1,
        text="Remove",
        command=lambda: remove_building(state, building_treeview),
    )
    remove_button.pack(side=tk.LEFT, padx=5, pady=5)

    building_treeview.bind(
        "<Button-1>", lambda e: on_click_edit(e, state, building_treeview)
    )

    # Section 2 - Selected Building's room list
    selected_building_label = ttk.Label(
        section2, text="Selected Building: ", font=("Arial", 14)
    )
    selected_building_label.pack(pady=10, anchor="w")

    room_treview_label = ttk.Label(
        section2, text="Room Treeview with Finish Type", font=("Arial", 14)
    )
    room_treview_label.pack(padx=20, pady=10, anchor="w")
    room_treview_label.config(cursor="question_arrow")
    room_treview_label_ttp = CreateToolTip(
        room_treview_label,
        """
>> Revit Summary(by Dynamo)의 Room 정보를 복사하여 붙여넣는 구간입니다.
------------------------------
* 이곳의 입력은 필수가 아니며, 레빗 모델링 내 룸 정보를 간편하게 붙여넣는 구간입니다.
======================
F91 / B35 / W02A / C95A
101 CENTRAL CONTROL ROOM
102 MEETING ROOM
103 ENGINEERING ROOM
======================
위와 같은 형식의 텍스트를 Revit Summary 에서 복사하여 붙여넣으면
자동으로 룸 넘버, 룸 이름, 룸 피니시 타입의 순서로 정리되어 항목이 추가 됩니다.

* 여기서 룸 정보를 입력하지 않더라도, 패밀리타입관리 > Room 탭에서
  사용자가 임의로 룸 피니시 타입을 생성하고, 룸을 추가할 수 있습니다.
        """,
    )

    room_treeview_frame = ttk.Frame(section2, width=300)
    room_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    room_treeview = create_treeview_forPjinfo(project_info_tab, state)
    room_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

    building_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: on_building_select(
            e, state, building_treeview, selected_building_label, room_treeview
        ),
    )

    new_room_text = tk.Text(room_treeview_frame, height=40, width=50)
    new_room_text.pack(pady=5)

    add_item_button = ttk.Button(
        room_treeview_frame,
        text="Add Items",
        command=lambda: add_item_in_roomTree(
            state, building_treeview, room_treeview, new_room_text
        ),
    )
    add_item_button.pack(side=tk.LEFT, padx=30, pady=5)

    remove_item_button = ttk.Button(
        room_treeview_frame,
        text="Remove Items",
        command=lambda: remove_item_in_roomTree(
            state, building_treeview, room_treeview
        ),
    )
    remove_item_button.pack(side=tk.LEFT, padx=5, pady=5)

    return project_info_tab
