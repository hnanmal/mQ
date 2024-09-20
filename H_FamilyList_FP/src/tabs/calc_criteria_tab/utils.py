# src/tabs/calc_criteria_tab/utils.py
import json
import tkinter as tk
from tkinter import filedialog


def on_cat_select(
    event,
    state,
    treeview1,
    label,
    treeview2,
):
    selected_item = treeview1.selection()
    if selected_item:
        selected_itemName = treeview1.item(selected_item[0])["values"][0]
        label.config(text=f"Selected Category: {selected_itemName}")
        treeview2.delete(*treeview2.get_children())

        for calcType_dic in state.project_info["calc_types"]:
            if selected_itemName == calcType_dic["category"]:
                treeview2.insert(
                    "",
                    "end",
                    values=(
                        calcType_dic["type_tag"],
                        calcType_dic["category"],
                    ),
                )

        state.logging_text_widget.write(
            f"[ {selected_itemName} ] 카테고리의 산출타입태그를 조회합니다.\n"
        )


def on_calcType_select(
    event,
    state,
    treeview1,
    treeview2,
    label,
    treeview3,
):
    selected_cat = treeview1.selection()
    selected_catName = treeview1.item(selected_cat)["values"][0]
    selected_item = treeview2.selection()
    selected_itemCat = treeview2.item(selected_item)["values"][1]

    if selected_item:
        treeview3.delete(*treeview3.get_children())
        selected_itemName = treeview2.item(selected_item)["values"][0]
        label.config(text=f"Selected Calc Type Tag: {selected_itemName}")

        for calcType_dic in state.project_info["calc_types"]:
            if selected_itemName == calcType_dic["type_tag"]:
                for formula_dic in calcType_dic["formulas"]:
                    treeview3.insert(
                        "",
                        "end",
                        values=(
                            formula_dic["formula"],
                            formula_dic["description"],
                            formula_dic["calc_type"],
                        ),
                    )

        state.logging_text_widget.write(
            f"[ {selected_itemName} ] 산출타입태그의 세부 항목을 조회합니다.\n"
        )


def add_calcType(state, cat_treeview, calcType_treeview, new_calcType_text):
    param_input = new_calcType_text.get("1.0", tk.END).strip()
    cat = cat_treeview.selection()[0]
    cat_name = cat_treeview.item(cat, "values")[0]
    if param_input:
        params = param_input.split("\n")
        for param in params:
            if param.strip():
                calcType_treeview.insert(
                    "",
                    "end",
                    values=(param, cat_name),
                )
                state.logging_text_widget.write(f"add [ {param} ] Calc Type tag.\n")
        new_calcType_text.delete("1.0", tk.END)


def remove_calcType(state, calcType_treeview):
    selected_items = calcType_treeview.selection()
    for item in selected_items:
        item_name = calcType_treeview.item(item, "values")[0]
        state.logging_text_widget.write(f"remove [ {item_name} ] Calc Type tag.\n")
        calcType_treeview.delete(item)


# 삽입, 삭제 시에 state.project_info를 수정하면서 가고,
# Save에서는 현재 state.project_info를 저장만 하도록 수정 요
def add_formula(state, calcType_treeview, stdFormula_treeview, new_formula_text):
    param_input = new_formula_text.get("1.0", tk.END).strip()
    calcType = calcType_treeview.selection()[0]
    calcType_name = calcType_treeview.item(calcType, "values")[0]
    if param_input:
        params = param_input.split("\n")
        for param in params:
            if param.strip():
                stdFormula_treeview.insert(
                    "",
                    "end",
                    values=(param, "", calcType_name),
                )
                state.logging_text_widget.write(f"add [ {param} ] Calc Type tag.\n")
        new_formula_text.delete("1.0", tk.END)


def remove_formula(state, stdFormula_treeview):
    selected_items = stdFormula_treeview.selection()
    for item in selected_items:
        item_name = stdFormula_treeview.item(item, "values")[0]
        state.logging_text_widget.write(f"remove [ {item_name} ] Calc Type tag.\n")
        stdFormula_treeview.delete(item)


def save_project_calcType_info(state, calcType_treeview, stdFormula_treeview):
    # Save project_info in the state

    # Function to retrieve all headers
    def get_treeview_headers(tree):
        headers = []
        for col in tree["columns"]:
            header = tree.heading(col)["text"]
            headers.append(header)
        return headers

    calcType_headers = get_treeview_headers(calcType_treeview)
    stdFormula_headers = get_treeview_headers(stdFormula_treeview)
    calc_types = []
    for item in calcType_treeview.get_children():
        tmp_calc = {}
        for k, v in zip(calcType_headers, calcType_treeview.item(item).get("values")):
            tmp_calc[k] = v
        tmp_calc["formulas"] = []
        for formula in stdFormula_treeview.get_children():
            if (
                calcType_treeview.item(item).get("values")[0]
                == stdFormula_treeview.item(formula).get("values")[2]
            ):
                tmp_formula = {}
                for k, v in zip(
                    stdFormula_headers, stdFormula_treeview.item(formula).get("values")
                ):
                    tmp_formula[k] = v
                tmp_calc["formulas"].append(tmp_formula)
        calc_types.append(tmp_calc)

    state.project_info["calc_types"] = calc_types
    project_info_ = state.project_info
    # earth_treeview.get_children()

    # Save to file
    # file_path = f"{project_info_['project_name']}_pjt_info.json"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Default file extension
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")
