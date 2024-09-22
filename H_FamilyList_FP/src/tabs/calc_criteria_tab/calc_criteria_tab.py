# src/tabs/calc_criteria_tab/calc_criteria_tab.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

# from src.tabs.project_info_tab.common_utils import save_project_info
from src.tabs.input_common_tab.utils import (
    add_common_param,
    create_defaultTreeview,
    save_project_common_info,
)
from src.tabs.project_info_tab.common_utils import on_click_edit, refresh_treeview
from src.tabs.calc_criteria_tab.utils import (
    add_calcType,
    add_formula,
    on_calcType_select,
    on_cat_select,
    on_click_edit_calcType,
    on_click_edit_formula,
    remove_calcType,
    remove_formula,
    save_project_calcType_info,
)


def create_calc_criteria_tab(notebook, state):
    state.edited_value = tk.StringVar(value="Initial Value")
    """Create the '공통 정보 입력' tab with two sections."""
    calc_criteria_tab = ttk.Frame(notebook)
    notebook.add(calc_criteria_tab, text="산출 기준")

    # Divide the tab into three sections (frames)
    section0 = ttk.Frame(calc_criteria_tab, height=70)
    section1 = ttk.Frame(calc_criteria_tab, width=100, height=200)
    section2 = ttk.Frame(calc_criteria_tab, width=100, height=200)
    section3 = ttk.Frame(calc_criteria_tab, width=500, height=200)
    section4 = ttk.Frame(calc_criteria_tab, width=500, height=200)
    section5 = ttk.Frame(calc_criteria_tab, width=500, height=200)

    section0.pack(side=tk.TOP, fill=tk.BOTH)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section4.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section5.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    save_load_btn_frame = ttk.Frame(section0, width=300)
    save_load_btn_frame.pack(pady=10, anchor="w")

    current_load_label = ttk.Label(
        save_load_btn_frame, textvariable=state["current_loaded_pjt"]
    )
    current_load_label.pack(side="top", padx=10, pady=10)

    save_info_button = ttk.Button(
        save_load_btn_frame,
        text="Save Project Info",
        command=lambda: save_project_calcType_info(
            state,
            cat_treeview,
            calcType_treeview,
            stdFormula_treeview,
            # modelParam_treeview,
            # manual_inputParam_treeview,
        ),
    )
    save_info_button.pack(side="left", padx=30, pady=10, anchor="w")

    # Category List Title
    category_list_label = ttk.Label(section1, text="Category List", font=("Arial", 14))
    category_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar
    cat_treeview_frame = ttk.Frame(section1, width=300)
    cat_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    cat_treeview = ttk.Treeview(
        cat_treeview_frame,
        columns=("Category Name",),
        show="headings",
        height=8,
    )

    cat_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    cat_treeview.heading("Category Name", text="Category Name")

    scrollbar = ttk.Scrollbar(
        cat_treeview_frame, orient=tk.VERTICAL, command=cat_treeview.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    cat_treeview.config(yscrollcommand=scrollbar.set)

    default_cat_list = [
        "Room",
        "Floors",
        "Roofs",
        "Walls",
        "St_Fdn",
        "St_Col",
        "St_Framing",
        "Ceilings",
        "Doors",
        "Windows",
        "Stairs",
        "Railings",
        "Generic",
    ]

    for i in default_cat_list:
        cat_treeview.insert(
            "",
            "end",
            values=(i),
        )

    # cat_treeview.selection_set(cat_treeview.get_children()[0])

    # Section 2 - Selected Category's Criteria list
    selected_Cat_label = ttk.Label(
        section2, text="Selected Category: ", font=("Arial", 14)
    )
    selected_Cat_label.pack(pady=10, anchor="w")

    calcTypeTag_label = ttk.Label(
        section2, text="Q'ty Calc Type Tag", font=("Arial", 14)
    )
    calcTypeTag_label.pack(padx=20, pady=10, anchor="w")

    calcType_treeview_frame = ttk.Frame(section2, width=300)
    calcType_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    calcType_treeview = create_defaultTreeview(
        state,
        calcType_treeview_frame,
        ("type_tag", "category"),
    )
    calcType_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

    cat_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: on_cat_select(
            e,
            state,
            cat_treeview,
            selected_Cat_label,
            calcType_treeview,
        ),
    )
    calcType_treeview.bind(
        "<Double-Button-1>",
        lambda e: on_click_edit_calcType(
            e,
            state,
            calcType_treeview,
        ),
    )

    new_calcType_text = tk.Text(section2, height=4, width=30)
    new_calcType_text.pack(pady=5, anchor="w")

    add_newCalcType_button = ttk.Button(
        section2,
        text="Add",
        command=lambda: add_calcType(
            state, cat_treeview, calcType_treeview, new_calcType_text
        ),
    )
    add_newCalcType_button.pack(side=tk.LEFT, padx=5, pady=5)

    del_selectedCalcType_button = ttk.Button(
        section2,
        text="Del",
        command=lambda: remove_calcType(state, calcType_treeview),
    )
    del_selectedCalcType_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Section 3 - Selected Calc type's formula list
    selected_calcType_label = ttk.Label(
        section3, text="Selected Q'ty Calc Type Tag: ", font=("Arial", 14)
    )
    selected_calcType_label.pack(pady=10, anchor="w")

    stdFormula_label = ttk.Label(section3, text="표준 수식 예시", font=("Arial", 14))
    stdFormula_label.pack(padx=20, pady=10, anchor="w")

    stdFormula_treeview_frame = ttk.Frame(section3, width=300)
    stdFormula_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    stdFormula_treeview = create_defaultTreeview(
        state,
        stdFormula_treeview_frame,
        (
            "formula",
            "description",
            "calc_type",
        ),
    )
    stdFormula_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

    calcType_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: on_calcType_select(
            e,
            state,
            cat_treeview,
            calcType_treeview,
            selected_calcType_label,
            stdFormula_treeview,
        ),
    )
    stdFormula_treeview.bind(
        "<Double-Button-1>",
        lambda e: on_click_edit_formula(
            e,
            state,
            stdFormula_treeview,
        ),
    )

    new_formula_text = tk.Text(section3, height=4, width=30)
    new_formula_text.pack(pady=5, anchor="w")

    add_new_formula_button = ttk.Button(
        section3,
        text="Add",
        command=lambda: add_formula(
            state, calcType_treeview, stdFormula_treeview, new_formula_text
        ),
    )
    add_new_formula_button.pack(side=tk.LEFT, padx=5, pady=5)

    del_selectedCalcType_button = ttk.Button(
        section3,
        text="Del",
        command=lambda: remove_formula(state, stdFormula_treeview),
    )
    del_selectedCalcType_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Section 4 - Selected Calc types's Model Parameter list
    modelParam_label = ttk.Label(section4, text="모델 Parameter", font=("Arial", 14))
    modelParam_label.pack(padx=20, pady=10, anchor="w")

    modelParam_treeview_frame = ttk.Frame(section4, width=300)
    modelParam_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    modelParam_treeview = create_defaultTreeview(
        state,
        modelParam_treeview_frame,
        ("항목", "수식 약자", "Parameter", "단위", "비고", "calc_type"),
    )
    modelParam_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

    # Section 5 - Selected Calc types's Manual Input Parameter list
    manual_inputParam_label = ttk.Label(
        section5, text="수동 입력값", font=("Arial", 14)
    )
    manual_inputParam_label.pack(padx=20, pady=10, anchor="w")

    manual_inputParam_treeview_frame = ttk.Frame(section5, width=300)
    manual_inputParam_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    manual_inputParam_treeview = create_defaultTreeview(
        state,
        manual_inputParam_treeview_frame,
        ("항목", "수식 약자", "수동입력값", "단위", "비고", "calc_type"),
    )
    manual_inputParam_treeview.pack(pady=10, fill=tk.BOTH, expand=True)
