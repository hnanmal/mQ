# src/tabs/calc_criteria_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Function to update Treeview items based on target_list
def update_manualParamTree_inputCommon(state, manual_Param_treeview):
    common_earth_items = state.project_info["common_info"]["earth"]
    common_earth_items_names = [
        common_earth_item["항목"] for common_earth_item in common_earth_items
    ]

    # Iterate through all items in the Treeview
    for tree_idx, item_id in enumerate(manual_Param_treeview.get_children()):
        # Get the value of the first column (index 0)
        calc_type = manual_Param_treeview.item(item_id, "values")[-1]
        first_column_value = manual_Param_treeview.item(item_id, "values")[0]
        for com_idx, item_name in enumerate(common_earth_items_names):
            if item_name == first_column_value:
                manual_Param_treeview.set(
                    item_id,
                    column="수동입력값",
                    value=common_earth_items[com_idx]["입력값"],
                )
                manual_Param_treeview.set(
                    item_id, column="단위", value=common_earth_items[com_idx]["단위"]
                )
                for calc_type_dic in state.project_info["calc_types"]:
                    if calc_type_dic["type_tag"] == calc_type:
                        calc_type_dic["manual_params"][tree_idx]["수동입력값"] = (
                            common_earth_items[com_idx]["입력값"]
                        )
                        calc_type_dic["manual_params"][tree_idx]["단위"] = (
                            common_earth_items[com_idx]["단위"]
                        )


# Function to handle in-place editing
def on_click_edit_calcType(
    event,
    # on_click_edit,
    state,
    calcType_treeview,
    # cat_treeview,
):
    selected_calcType = calcType_treeview.selection()[0]
    selected_calcType_name = calcType_treeview.item(selected_calcType)["values"][0]
    # selected_calcType_cat = calcType_treeview.item(selected_calcType)["values"][1]

    # Identify which item and column were clicked
    region = calcType_treeview.identify_region(event.x, event.y)
    if region == "cell":
        column = calcType_treeview.identify_column(event.x)
        row = calcType_treeview.identify_row(event.y)

        # Get the item ID and current value of the clicked cell
        item_id = calcType_treeview.identify_row(event.y)
        col_num = (
            int(column.replace("#", "")) - 1
        )  # Treeview columns are numbered as #1, #2, ...
        current_value = calcType_treeview.item(item_id, "values")[col_num]

        # Get the bounding box of the cell
        x, y, width, height = calcType_treeview.bbox(item_id, column)

        # Create an Entry widget over the cell
        entry = ttk.Entry(calcType_treeview)
        entry.place(x=x, y=y, width=width, height=height)

        # Insert the current value into the Entry widget
        entry.insert(0, current_value)
        entry.focus()

        # Save the new value when Enter is pressed or focus is lost
        def save_edit(state, event=None):
            new_value = entry.get()
            values = list(calcType_treeview.item(item_id, "values"))
            values[col_num] = new_value
            calcType_treeview.item(
                item_id, values=values
            )  # Update the treeview with the new value
            entry.destroy()  # Remove the Entry widget after saving
            state.edited_value.set(new_value)
            print(state.edited_value.get())
            # return new_value

            calc_type_dic_keys = ["type_tag", "설명", "category"]
            for calc_type_dic in state.project_info["calc_types"]:
                if calc_type_dic["type_tag"] == selected_calcType_name:
                    calc_type_dic[calc_type_dic_keys[col_num]] = new_value
                    if col_num == 0:
                        for formula_dic in calc_type_dic["formulas"]:
                            formula_dic["calc_type"] = new_value

        entry.bind(
            "<Return>", lambda e: save_edit(state, e)
        )  # Save when Enter is pressed
        entry.bind(
            "<FocusOut>", lambda e: save_edit(state, e)
        )  # Save when focus is lost


# Function to handle in-place editing
def on_click_edit_formula(
    event,
    # on_click_edit,
    state,
    stdFormula_treeview,
    # cat_treeview,
):
    selected_formula = stdFormula_treeview.selection()[0]
    selected_formula_name = stdFormula_treeview.item(selected_formula)["values"][0]
    # selected_calcType_cat = stdFormula_treeview.item(selected_formula)["values"][1]

    # Identify which item and column were clicked
    region = stdFormula_treeview.identify_region(event.x, event.y)
    if region == "cell":
        column = stdFormula_treeview.identify_column(event.x)
        row = stdFormula_treeview.identify_row(event.y)

        # Get the item ID and current value of the clicked cell
        item_id = stdFormula_treeview.identify_row(event.y)
        col_num = (
            int(column.replace("#", "")) - 1
        )  # Treeview columns are numbered as #1, #2, ...
        current_value = stdFormula_treeview.item(item_id, "values")[col_num]

        # Get the bounding box of the cell
        x, y, width, height = stdFormula_treeview.bbox(item_id, column)

        # Create an Entry widget over the cell
        entry = ttk.Entry(stdFormula_treeview)
        entry.place(x=x, y=y, width=width, height=height)

        # Insert the current value into the Entry widget
        entry.insert(0, current_value)
        entry.focus()

        # Save the new value when Enter is pressed or focus is lost
        def save_edit(state, event=None):
            new_value = entry.get()
            values = list(stdFormula_treeview.item(item_id, "values"))
            values[col_num] = new_value
            stdFormula_treeview.item(
                item_id, values=values
            )  # Update the treeview with the new value
            entry.destroy()  # Remove the Entry widget after saving
            state.edited_value.set(new_value)
            print(state.edited_value.get())
            # return new_value

            for calc_type_dic in state.project_info["calc_types"]:
                for formula_dic in calc_type_dic["formulas"]:
                    formula_dic_keys = list(formula_dic.keys())
                    if formula_dic["formula"] == selected_formula_name:
                        formula_dic[formula_dic_keys[col_num]] = new_value

        entry.bind(
            "<Return>", lambda e: save_edit(state, e)
        )  # Save when Enter is pressed
        entry.bind(
            "<FocusOut>", lambda e: save_edit(state, e)
        )  # Save when focus is lost


def on_click_edit_modelParam(
    event,
    # on_click_edit,
    state,
    modelParam_treeview,
    # cat_treeview,
):
    selected_modelParam = modelParam_treeview.selection()[0]
    selected_modelParam_name = modelParam_treeview.item(selected_modelParam)["values"][
        0
    ]
    # selected_calcType_cat = stdFormula_treeview.item(selected_formula)["values"][1]

    # Identify which item and column were clicked
    region = modelParam_treeview.identify_region(event.x, event.y)
    if region == "cell":
        column = modelParam_treeview.identify_column(event.x)
        row = modelParam_treeview.identify_row(event.y)

        # Get the item ID and current value of the clicked cell
        item_id = modelParam_treeview.identify_row(event.y)
        col_num = (
            int(column.replace("#", "")) - 1
        )  # Treeview columns are numbered as #1, #2, ...
        current_value = modelParam_treeview.item(item_id, "values")[col_num]

        # Get the bounding box of the cell
        x, y, width, height = modelParam_treeview.bbox(item_id, column)

        # Create an Entry widget over the cell
        entry = ttk.Entry(modelParam_treeview)
        entry.place(x=x, y=y, width=width, height=height)

        # Insert the current value into the Entry widget
        entry.insert(0, current_value)
        entry.focus()

        # Save the new value when Enter is pressed or focus is lost
        def save_edit(state, event=None):
            new_value = entry.get()
            values = list(modelParam_treeview.item(item_id, "values"))
            values[col_num] = new_value
            modelParam_treeview.item(
                item_id, values=values
            )  # Update the treeview with the new value
            entry.destroy()  # Remove the Entry widget after saving
            state.edited_value.set(new_value)
            print(state.edited_value.get())
            # return new_value

            for calc_type_dic in state.project_info["calc_types"]:
                for modelParam_dic in calc_type_dic["model_params"]:
                    modelParam_dic_keys = list(modelParam_dic.keys())
                    if modelParam_dic["항목"] == selected_modelParam_name:
                        modelParam_dic[modelParam_dic_keys[col_num]] = new_value

        entry.bind(
            "<Return>", lambda e: save_edit(state, e)
        )  # Save when Enter is pressed
        entry.bind(
            "<FocusOut>", lambda e: save_edit(state, e)
        )  # Save when focus is lost


def on_click_edit_manual_Param(
    event,
    # on_click_edit,
    state,
    manual_Param_treeview,
    # cat_treeview,
):
    selected_modelParam = manual_Param_treeview.selection()[0]
    selected_modelParam_name = manual_Param_treeview.item(selected_modelParam)[
        "values"
    ][0]
    # selected_calcType_cat = stdFormula_treeview.item(selected_formula)["values"][1]

    # Identify which item and column were clicked
    region = manual_Param_treeview.identify_region(event.x, event.y)
    if region == "cell":
        column = manual_Param_treeview.identify_column(event.x)
        row = manual_Param_treeview.identify_row(event.y)

        # Get the item ID and current value of the clicked cell
        item_id = manual_Param_treeview.identify_row(event.y)
        col_num = (
            int(column.replace("#", "")) - 1
        )  # Treeview columns are numbered as #1, #2, ...
        current_value = manual_Param_treeview.item(item_id, "values")[col_num]

        # Get the bounding box of the cell
        x, y, width, height = manual_Param_treeview.bbox(item_id, column)

        # Create an Entry widget over the cell
        entry = ttk.Entry(manual_Param_treeview)
        entry.place(x=x, y=y, width=width, height=height)

        # Insert the current value into the Entry widget
        entry.insert(0, current_value)
        entry.focus()

        # Save the new value when Enter is pressed or focus is lost
        def save_edit(state, event=None):
            new_value = entry.get()
            values = list(manual_Param_treeview.item(item_id, "values"))
            values[col_num] = new_value
            manual_Param_treeview.item(
                item_id, values=values
            )  # Update the treeview with the new value
            entry.destroy()  # Remove the Entry widget after saving
            state.edited_value.set(new_value)
            print(state.edited_value.get())
            # return new_value

            for calc_type_dic in state.project_info["calc_types"]:
                for manualParam_dic in calc_type_dic["manual_params"]:
                    manualParam_dic_keys = list(manualParam_dic.keys())
                    if manualParam_dic["항목"] == selected_modelParam_name:
                        manualParam_dic[manualParam_dic_keys[col_num]] = new_value

        entry.bind(
            "<Return>", lambda e: save_edit(state, e)
        )  # Save when Enter is pressed
        entry.bind(
            "<FocusOut>", lambda e: save_edit(state, e)
        )  # Save when focus is lost


def on_cat_select(
    event,
    state,
    cat_treeview,
    selected_Cat_label,
    selected_calcType_label,
    calcType_treeview,
    stdFormula_treeview,
    modelParam_treeview,
    manual_Param_treeview,
):
    selected_item = cat_treeview.selection()
    if selected_item:
        selected_itemName = cat_treeview.item(selected_item[0])["values"][0]
        selected_Cat_label.config(text=f"Selected Category: {selected_itemName}")
        selected_calcType_label.config(text=f"Selected Calc Type Tag:       ")
        calcType_treeview.delete(*calcType_treeview.get_children())
        stdFormula_treeview.delete(*stdFormula_treeview.get_children())
        modelParam_treeview.delete(*modelParam_treeview.get_children())
        manual_Param_treeview.delete(*manual_Param_treeview.get_children())

        for calcType_dic in state.project_info["calc_types"]:
            if selected_itemName == calcType_dic["category"]:
                calcType_treeview.insert(
                    "",
                    "end",
                    values=(
                        calcType_dic["type_tag"],
                        calcType_dic["설명"],
                        calcType_dic["category"],
                    ),
                )

        state.logging_text_widget.write(
            f"[ {selected_itemName} ] 카테고리의 산출타입태그를 조회합니다.\n"
        )


def on_calcType_select(
    event,
    state,
    cat_treeview,
    calcType_treeview,
    label,
    stdFormula_treeview,
    modelParam_treeview,
    manual_Param_treeview,
):
    # selected_cat = cat_treeview.selection()
    # selected_catName = cat_treeview.item(selected_cat)["values"][0]
    selected_item = calcType_treeview.selection()
    # selected_itemCat = calcType_treeview.item(selected_item)["values"][-1]

    if selected_item:
        stdFormula_treeview.delete(*stdFormula_treeview.get_children())
        modelParam_treeview.delete(*modelParam_treeview.get_children())
        manual_Param_treeview.delete(*manual_Param_treeview.get_children())
        selected_itemName = calcType_treeview.item(selected_item)["values"][0]
        label.config(text=f"Selected Calc Type Tag: {selected_itemName}")

        for calcType_dic in state.project_info["calc_types"]:
            if selected_itemName == calcType_dic["type_tag"]:
                for formula_dic in calcType_dic["formulas"]:
                    stdFormula_treeview.insert(
                        "",
                        "end",
                        values=(
                            formula_dic["formula"],
                            formula_dic["description"],
                            formula_dic["calc_type"],
                        ),
                    )
                for modelParam_dic in calcType_dic["model_params"]:
                    modelParam_treeview.insert(
                        "",
                        "end",
                        values=(
                            modelParam_dic["항목"],
                            modelParam_dic["수식 약자"],
                            modelParam_dic["Parameter"],
                            modelParam_dic["단위"],
                            modelParam_dic["비고"],
                            modelParam_dic["calc_type"],
                        ),
                    )
                for manualParam_dic in calcType_dic["manual_params"]:
                    manual_Param_treeview.insert(
                        "",
                        "end",
                        values=(
                            manualParam_dic["항목"],
                            manualParam_dic["수식 약자"],
                            manualParam_dic["수동입력값"],
                            manualParam_dic["단위"],
                            manualParam_dic["비고"],
                            manualParam_dic["calc_type"],
                        ),
                    )

        state.logging_text_widget.write(
            f"[ {selected_itemName} ] 산출타입태그의 세부 항목을 조회합니다.\n"
        )


def add_calcType(state, cat_treeview, calcType_treeview, new_calcType_text):
    calcType_input = new_calcType_text.get("1.0", tk.END).strip()
    cat = cat_treeview.selection()[0]
    cat_name = cat_treeview.item(cat, "values")[0]
    if calcType_input:
        calcTypes = calcType_input.split("\n")
        for calcType in calcTypes:
            if calcType.strip():
                calcType_treeview.insert(
                    "",
                    "end",
                    values=(calcType, "", cat_name),
                )
                state.project_info["calc_types"].append(
                    {
                        "type_tag": calcType,
                        "설명": "",
                        "category": cat_name,
                        "formulas": [],
                        "model_params": [],
                        "manual_params": [],
                    }
                )
                state.logging_text_widget.write(f"add [ {calcType} ] Calc Type tag.\n")
        new_calcType_text.delete("1.0", tk.END)


def remove_calcType(state, calcType_treeview):
    selected_calcTypes = calcType_treeview.selection()
    for selected_calcType in selected_calcTypes:
        selected_calcType_name = calcType_treeview.item(selected_calcType, "values")[0]
        state.logging_text_widget.write(
            f"remove [ {selected_calcType_name} ] Calc Type tag.\n"
        )

        for calcType_dic in state.project_info["calc_types"]:
            if calcType_dic["type_tag"] == selected_calcType_name:
                state.project_info["calc_types"].remove(calcType_dic)

        calcType_treeview.delete(selected_calcType)


def add_formula(state, calcType_treeview, stdFormula_treeview, new_formula_text):
    formula_input = new_formula_text.get("1.0", tk.END).strip()
    calcType = calcType_treeview.selection()[0]
    calcType_name = calcType_treeview.item(calcType, "values")[0]

    if formula_input:
        formulas = formula_input.split("\n")
        for formula in formulas:
            if formula.strip():
                # # state 저장
                for idx, calcType in enumerate(state.project_info["calc_types"]):
                    if calcType_name == calcType["type_tag"]:
                        calcType["formulas"].append(
                            {
                                "formula": formula,
                                "description": "",
                                "calc_type": calcType_name,
                            }
                        )

                # 트리뷰 저장
                stdFormula_treeview.insert(
                    "",
                    "end",
                    values=(formula, "", calcType_name),
                )
                state.logging_text_widget.write(f"add [ {formula} ] 산출식.\n")
        new_formula_text.delete("1.0", tk.END)


def remove_formula(state, stdFormula_treeview, calcType_treeview):
    selected_calcType = calcType_treeview.selection()[0]
    selected_calcType_name = calcType_treeview.item(selected_calcType, "values")[0]
    selected_formulas = stdFormula_treeview.selection()
    for selected_formula in selected_formulas:
        selected_formula_name = stdFormula_treeview.item(selected_formula, "values")[0]
        state.logging_text_widget.write(
            f"remove [ {selected_formula_name} ] Calc Type tag.\n"
        )

        for idx, calcType_dic in enumerate(state.project_info["calc_types"]):
            if calcType_dic["type_tag"] == selected_calcType_name:
                for formula_dic in calcType_dic["formulas"]:
                    if formula_dic["formula"] == selected_formula_name:
                        state.project_info["calc_types"][idx]["formulas"].remove(
                            formula_dic
                        )

        stdFormula_treeview.delete(selected_formula)


def add_modelParam(state, calcType_treeview, modelParam_treeview, new_modelParam_text):
    modelParam_input = new_modelParam_text.get("1.0", tk.END).strip()
    calcType = calcType_treeview.selection()[0]
    calcType_name = calcType_treeview.item(calcType, "values")[0]

    if modelParam_input:
        modelParams = modelParam_input.split("\n")
        for modelParam in modelParams:
            if modelParam.strip():
                col_list_ = ["항목", "수식 약자", "Parameter", "단위", "비고"]
                input_cnt = len(modelParam.split(","))
                col_list = col_list_[: input_cnt + 1]
                input_dict = dict(zip(col_list, modelParam.split(",")))
                # # state 저장
                for idx, calcType in enumerate(state.project_info["calc_types"]):
                    if calcType_name == calcType["type_tag"]:
                        calcType["model_params"].append(
                            {
                                "항목": input_dict["항목"],
                                "수식 약자": (
                                    input_dict["수식 약자"]
                                    if input_dict.get("수식 약자")
                                    else ""
                                ),
                                "Parameter": (
                                    input_dict["Parameter"]
                                    if input_dict.get("Parameter")
                                    else ""
                                ),
                                "단위": (
                                    input_dict["단위"] if input_dict.get("단위") else ""
                                ),
                                "비고": (
                                    input_dict["비고"] if input_dict.get("비고") else ""
                                ),
                                "calc_type": calcType_name,
                            }
                        )

                # 트리뷰 저장
                modelParam_treeview.insert(
                    "",
                    "end",
                    values=(
                        input_dict["항목"] if input_dict.get("항목") else "",
                        input_dict["수식 약자"] if input_dict.get("수식 약자") else "",
                        input_dict["Parameter"] if input_dict.get("Parameter") else "",
                        input_dict["단위"] if input_dict.get("단위") else "",
                        input_dict["비고"] if input_dict.get("비고") else "",
                        calcType_name,
                    ),
                )
                state.logging_text_widget.write(
                    f"add [ {modelParam} ] 모델 파라미터.\n"
                )
        new_modelParam_text.delete("1.0", tk.END)


def remove_modelParam(state, modelParam_treeview, calcType_treeview):
    selected_calcType = calcType_treeview.selection()[0]
    selected_calcType_name = calcType_treeview.item(selected_calcType, "values")[0]
    selected_modelParams = modelParam_treeview.selection()
    for selected_modelParam in selected_modelParams:
        selected_modelParam_name = modelParam_treeview.item(
            selected_modelParam, "values"
        )[0]
        state.logging_text_widget.write(
            f"remove [ {selected_modelParam_name} ] Calc Type tag.\n"
        )

        for idx, calcType_dic in enumerate(state.project_info["calc_types"]):
            if calcType_dic["type_tag"] == selected_calcType_name:
                for model_param_dic in calcType_dic["model_params"]:
                    if model_param_dic["항목"] == selected_modelParam_name:
                        state.project_info["calc_types"][idx]["model_params"].remove(
                            model_param_dic
                        )

        modelParam_treeview.delete(selected_modelParam)


def add_manualParam(
    state, calcType_treeview, manual_Param_treeview, new_manualParam_text
):
    manualParam_input = new_manualParam_text.get("1.0", tk.END).strip()
    calcType = calcType_treeview.selection()[0]
    calcType_name = calcType_treeview.item(calcType, "values")[0]

    if manualParam_input:
        manualParams = manualParam_input.split("\n")
        for manualParam in manualParams:
            if manualParam.strip():
                col_list_ = ["항목", "수식 약자", "수동입력값", "단위", "비고"]
                input_cnt = len(manualParam.split(","))
                col_list = col_list_[: input_cnt + 1]
                input_dict = dict(zip(col_list, manualParam.split(",")))
                # # state 저장
                for idx, calcType in enumerate(state.project_info["calc_types"]):
                    if calcType_name == calcType["type_tag"]:
                        calcType["manual_params"].append(
                            {
                                "항목": input_dict["항목"],
                                "수식 약자": (
                                    input_dict["수식 약자"]
                                    if input_dict.get("수식 약자")
                                    else ""
                                ),
                                "수동입력값": (
                                    input_dict["수동입력값"]
                                    if input_dict.get("수동입력값")
                                    else ""
                                ),
                                "단위": (
                                    input_dict["단위"] if input_dict.get("단위") else ""
                                ),
                                "비고": (
                                    input_dict["비고"] if input_dict.get("비고") else ""
                                ),
                                "calc_type": calcType_name,
                            }
                        )

                # 트리뷰 저장
                manual_Param_treeview.insert(
                    "",
                    "end",
                    values=(
                        input_dict["항목"] if input_dict.get("항목") else "",
                        input_dict["수식 약자"] if input_dict.get("수식 약자") else "",
                        (
                            input_dict["수동입력값"]
                            if input_dict.get("수동입력값")
                            else ""
                        ),
                        input_dict["단위"] if input_dict.get("단위") else "",
                        input_dict["비고"] if input_dict.get("비고") else "",
                        calcType_name,
                    ),
                )
                state.logging_text_widget.write(
                    f"add [ {manualParam} ] 수동입력 파라미터.\n"
                )
        new_manualParam_text.delete("1.0", tk.END)


def remove_manualParam(state, manual_Param_treeview, calcType_treeview):
    selected_calcType = calcType_treeview.selection()[0]
    selected_calcType_name = calcType_treeview.item(selected_calcType, "values")[0]
    selected_manualParams = manual_Param_treeview.selection()
    for selected_manualParam in selected_manualParams:
        selected_manualParam_name = manual_Param_treeview.item(
            selected_manualParam, "values"
        )[0]
        state.logging_text_widget.write(
            f"remove [ {selected_manualParam_name} ] 수동입력 파라미터.\n"
        )

        for idx, calcType_dic in enumerate(state.project_info["calc_types"]):
            if calcType_dic["type_tag"] == selected_calcType_name:
                for manual_param_dic in calcType_dic["manual_params"]:
                    if manual_param_dic["항목"] == selected_manualParam_name:
                        state.project_info["calc_types"][idx]["manual_params"].remove(
                            manual_param_dic
                        )

        manual_Param_treeview.delete(selected_manualParam)


def save_project_calcType_info(state):
    project_info_ = state.project_info

    file_path = filedialog.asksaveasfilename(
        defaultextension=".hpjt",  # Default file extension
        filetypes=[("HPJT files", "*.hpjt"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")
