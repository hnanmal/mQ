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
    add_manualParam,
    add_modelParam,
    on_calcType_select,
    on_cat_select,
    on_click_edit_calcType,
    on_click_edit_formula,
    on_click_edit_manual_Param,
    on_click_edit_modelParam,
    remove_calcType,
    remove_formula,
    remove_manualParam,
    remove_modelParam,
    save_project_calcType_info,
    update_manualParamTree_inputCommon,
)


def create_calc_criteria_tab(notebook, state):
    state.edited_value = tk.StringVar(value="Initial Value")
    """Create the '공통 정보 입력' tab with two sections."""
    calc_criteria_tab = ttk.Frame(notebook)
    notebook.add(calc_criteria_tab, text="산출 기준")

    # s = ttk.Style()
    # s.configure("new.TFrame", background="#7AC5CD")

    # Divide the tab into three sections (frames)
    bigArea1 = ttk.Frame(calc_criteria_tab, width=500, height=200)
    bigArea2 = ttk.Frame(calc_criteria_tab, width=300, height=200)
    bigArea1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    bigArea2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    section0 = ttk.Frame(bigArea1, height=70)
    section1 = ttk.Frame(bigArea1, width=30, height=200)
    section2 = ttk.Frame(bigArea1, width=100, height=200)
    section3 = ttk.Frame(bigArea1, width=500, height=200)
    section4 = ttk.Frame(bigArea2, width=500, height=100)
    section5 = ttk.Frame(bigArea2, width=500, height=200)

    section0.pack(side=tk.TOP, anchor="w", fill=tk.X)
    section1.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.Y, expand=True)
    section2.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section3.pack(side=tk.LEFT, padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)
    section4.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=True)
    section5.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

    save_load_btn_frame = ttk.Frame(section0, width=100)
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

    # Category List Title
    category_list_label = ttk.Label(section1, text="Category List", font=("Arial", 14))
    category_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar
    cat_treeview_frame = ttk.Frame(section1, width=30)
    cat_treeview_frame.pack(pady=10, fill=tk.Y, expand=True)

    cat_treeview = ttk.Treeview(
        cat_treeview_frame,
        columns=("Category Name",),
        show="headings",
        height=8,
    )

    cat_treeview.pack(side=tk.LEFT, fill=tk.Y, expand=True)
    cat_treeview.heading("Category Name", text="Category")
    cat_treeview.column("#0", width=50)

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
        section2, text="Selected Category:         ", font=("Arial", 13)
    )
    selected_Cat_label.pack(pady=10, anchor="w")

    calcTypeTag_label = ttk.Label(
        section2, text="Q'ty Calc Type Tag", font=("Arial", 12)
    )
    calcTypeTag_label.pack(padx=20, pady=10, anchor="w")

    calcType_treeview_frame = ttk.Frame(section2, width=300)
    calcType_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    calcType_treeview = create_defaultTreeview(
        state,
        calcType_treeview_frame,
        ("type_tag", "설명", "category"),
    )
    calcType_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

    cat_treeview.bind(
        "<<TreeviewSelect>>",
        lambda e: on_cat_select(
            e,
            state,
            cat_treeview,
            selected_Cat_label,
            selected_calcType_label,
            calcType_treeview,
            stdFormula_treeview,
            modelParam_treeview,
            manual_Param_treeview,
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
        section3, text="Selected Calc Type Tag:       ", font=("Arial", 12)
    )
    selected_calcType_label.pack(pady=10, anchor="w")

    stdFormula_label = ttk.Label(section3, text="표준 수식", font=("Arial", 14))
    stdFormula_label.pack(padx=20, pady=10, anchor="w")

    # smallfont = tk.font.Font(size=11)

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
    # Set column properties
    stdFormula_treeview.column(
        "formula", anchor="w", width=200
    )  # Align text to the left (west)
    stdFormula_treeview.column(
        "description", anchor="w", width=200
    )  # Align text to the left (west)
    stdFormula_treeview.column(
        "calc_type", anchor="w", width=50
    )  # Align text to the left (west)
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
            modelParam_treeview,
            manual_Param_treeview,
        ),
    )
    stdFormula_treeview.bind(
        "<Double-Button-1>",
        lambda e: on_click_edit_formula(
            e,
            state,
            stdFormula_treeview,
            calcType_treeview,
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

    del_selected_formula_button = ttk.Button(
        section3,
        text="Del",
        command=lambda: remove_formula(state, stdFormula_treeview, calcType_treeview),
    )
    del_selected_formula_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Section 4 - Selected Calc types's Model Parameter list
    modelParam_label = ttk.Label(
        section4, text="모델 Parameter", font=("Arial", 14, "bold")
    )
    modelParam_label.pack(padx=20, pady=10, anchor="w")

    modelParam_treeview_frame = ttk.Frame(section4, width=300, height=100)
    modelParam_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    modelParam_treeview = create_defaultTreeview(
        state,
        modelParam_treeview_frame,
        ("항목", "수식 약자", "Parameter", "단위", "비고", "calc_type"),
        height=5,
    )
    modelParam_treeview.pack(pady=10, fill=tk.X, expand=True)

    modelParam_treeview.bind(
        "<Double-Button-1>",
        lambda e: on_click_edit_modelParam(
            e,
            state,
            modelParam_treeview,
            calcType_treeview,
        ),
    )

    new_modelParam_text = tk.Text(section4, height=2, width=100)
    new_modelParam_text.pack(side=tk.RIGHT, pady=5, anchor="e")

    add_new_modelParam_button = ttk.Button(
        section4,
        text="Add",
        command=lambda: add_modelParam(
            state, calcType_treeview, modelParam_treeview, new_modelParam_text
        ),
    )
    add_new_modelParam_button.pack(side=tk.LEFT, padx=5, pady=5)

    del_selected_modelParam_button = ttk.Button(
        section4,
        text="Del",
        command=lambda: remove_modelParam(
            state, modelParam_treeview, calcType_treeview
        ),
    )
    del_selected_modelParam_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Section 5 - Selected Calc types's Manual Input Parameter list

    manual_Param_labelArea = ttk.Frame(section5, height=70)
    manual_Param_labelArea.pack(side=tk.TOP, anchor="w")
    manual_Param_label = ttk.Label(
        manual_Param_labelArea, text="수동 입력값", font=("Arial", 14, "bold")
    )
    manual_Param_label.pack(side=tk.LEFT, padx=20, pady=10, anchor="w")
    update_manualParam_common_button = ttk.Button(
        manual_Param_labelArea,
        text="Update Common Items",
        command=lambda: update_manualParamTree_inputCommon(
            state, manual_Param_treeview
        ),
    )
    update_manualParam_common_button.pack(side=tk.RIGHT, padx=20, pady=10, anchor="e")

    manual_Param_treeview_frame = ttk.Frame(section5, width=300, height=100)
    manual_Param_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    manual_Param_treeview = create_defaultTreeview(
        state,
        manual_Param_treeview_frame,
        ("항목", "수식 약자", "수동입력값", "단위", "비고", "calc_type"),
        height=8,
    )
    manual_Param_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

    manual_Param_treeview.bind(
        "<Double-Button-1>",
        lambda e: on_click_edit_manual_Param(
            e,
            state,
            manual_Param_treeview,
            calcType_treeview,
        ),
    )

    new_manualParam_text = tk.Text(section5, height=2, width=100)
    new_manualParam_text.pack(side=tk.RIGHT, pady=5, anchor="e")

    add_new_manualParam_button = ttk.Button(
        section5,
        text="Add",
        command=lambda: add_manualParam(
            state, calcType_treeview, manual_Param_treeview, new_manualParam_text
        ),
    )
    add_new_manualParam_button.pack(side=tk.LEFT, padx=5, pady=5)

    del_selected_manualParam_button = ttk.Button(
        section5,
        text="Del",
        command=lambda: remove_manualParam(
            state, manual_Param_treeview, calcType_treeview
        ),
    )
    del_selected_manualParam_button.pack(side=tk.LEFT, padx=5, pady=5)
