# src/views/project_info_tab/bd_treeview_utils.py
import tkinter as tk
from tkinter import ttk


def auto_numbering(state, building_treeview):
    items = building_treeview.get_children()
    if not items:
        return  # Do nothing if there are no items

    start_number = 1
    first_item_values = building_treeview.item(items[0], "values")
    if first_item_values[1]:  # If the first item has a number, start from it
        try:
            start_number = int(first_item_values[1])
        except ValueError:
            pass  # If it's not a valid number, start from 1

    for idx, item in enumerate(items):
        building_name = building_treeview.item(item, "values")[0]
        building_treeview.set(item, "Number", start_number + idx)

        # Update the building list in the state with new numbers
        if building_name in state.project_info["building_list"]:
            state.project_info["building_list"][building_name]["building_number"] = (
                start_number + idx
            )


def add_building(state, building_treeview, new_building_text):
    building_input = new_building_text.get("1.0", tk.END).strip()
    if building_input:
        buildings = building_input.split("\n")
        for building in buildings:
            if building.strip():
                building_name = building.strip()
                state.project_info["building_list"].append(
                    {
                        "building_name": building_name,
                        "building_number": None,
                        "finish_types": [],
                    }
                )
                building_treeview.insert("", "end", values=(building_name, ""))
                state.logging_text_widget.write(f"add [ {building_name} ] building.\n")
        new_building_text.delete("1.0", tk.END)


def remove_building(state, building_treeview):
    selected_items = building_treeview.selection()
    print(selected_items)
    for item in selected_items:
        building_name = building_treeview.item(item, "values")[0]
        state.logging_text_widget.write(f"remove [ {building_name} ] building.\n")
        for idx, value in enumerate(state.project_info["building_list"]):
            if building_name == value["building_name"]:
                del state.project_info["building_list"][idx]
        # state.project_info["building_list"].remove(
        #     {

        #     }
        # )

        building_treeview.delete(item)


def on_click_edit(event, state, building_treeview):
    if building_treeview.selection():
        selected_item = building_treeview.selection()[0]
        column = building_treeview.identify_column(event.x)
        if column == "#2":
            x, y, width, height = building_treeview.bbox(selected_item, "Number")
            entry = ttk.Entry(building_treeview)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, building_treeview.item(selected_item, "values")[1])

            def save_edit(event=None):
                building_treeview.set(selected_item, column="Number", value=entry.get())
                entry.destroy()

            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", save_edit)
            entry.focus()


# Add Treeview Selection Binding
def on_building_select(
    event, state, building_treeview, selected_building_label, room_treeview
):
    selected_item = building_treeview.selection()
    building_name = building_treeview.item(selected_item[0], "values")[0]
    if selected_item:
        selected_building = building_treeview.item(selected_item[0])["values"][0]
        selected_building_label.config(text=f"Selected Building: {selected_building}")
        room_treeview.delete(*room_treeview.get_children())

        for building_dic in state.project_info["building_list"]:
            if building_name == building_dic["building_name"]:
                for room_dic in building_dic["room_list"]:
                    room_treeview.insert(
                        "",
                        "end",
                        text=room_dic["room_no"],
                        values=(room_dic["room_name"], room_dic["finish_type"]),
                    )

        state.logging_text_widget.write(
            f"[ {building_name} ] 빌딩의 피니시 타입을 조회합니다.\n"
        )
