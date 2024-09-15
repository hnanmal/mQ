# src/views/project_info_tab/finishType_list_utils.py
import tkinter as tk


# Add Finish Type functionality
def add_finish_type(state, building_treeview, finish_listbox, new_finish_text):
    finish_type = new_finish_text.get("1.0", tk.END).strip()

    if finish_type:
        selected_item = building_treeview.selection()
        if selected_item:
            building_name = building_treeview.item(selected_item[0], "values")[0]
            finish_listbox.insert(tk.END, finish_type)

            # Update state for the selected building
            if "finish_types" not in state.project_info["building_list"][building_name]:
                state.project_info["building_list"][building_name]["finish_types"] = []
            state.project_info["building_list"][building_name]["finish_types"].append(
                finish_type
            )

            new_finish_text.delete("1.0", tk.END)
    print(state.project_info)


def remove_finish_type(state, building_treeview, finish_listbox):
    selected_item = building_treeview.selection()
    building_name = building_treeview.item(selected_item[0], "values")[0]
    selected_items = finish_listbox.curselection()
    for item in selected_items:
        state.logging_text_widget.write(f"remove {finish_listbox.get(item)}")
        state.project_info["building_list"][building_name]["finish_types"].remove(
            state.project_info["building_list"][building_name]["finish_types"][item]
        )
        finish_listbox.delete(item)
