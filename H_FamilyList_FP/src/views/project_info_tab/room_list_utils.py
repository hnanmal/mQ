# src/views/project_info_tab/room_list_utils.py
import tkinter as tk


# Add room functionality
def add_room(state, building_treeview, finish_listbox, room_listbox, new_room_text):
    room_input = new_room_text.get("1.0", tk.END).strip()

    if room_input:
        rooms = room_input.split("\n")
        selected_item = finish_listbox.selection()
        for room in rooms:
            room_no, room_name = room.split("\t")
        if selected_item:
            finishType_name = finish_listbox.item(selected_item[0], "values")[0]
            room_listbox.insert(tk.END, room)

            # Update state for the selected building
            if "finish_types" not in state.project_info["building_list"][building_name]:
                state.project_info["building_list"][building_name]["finish_types"] = []
            state.project_info["building_list"][building_name]["finish_types"].append(
                room
            )

            new_room_text.delete("1.0", tk.END)
    print(state.project_info)


def remove_room(state, building_treeview, finish_listbox, room_listbox):
    selected_item = building_treeview.selection()
    building_name = building_treeview.item(selected_item[0], "values")[0]
    selected_items = room_listbox.curselection()
    for item in selected_items:
        state.logging_text_widget.write(f"remove {room_listbox.get(item)}")
        state.project_info["building_list"][building_name]["finish_types"].remove(
            state.project_info["building_list"][building_name]["finish_types"][item]
        )
        room_listbox.delete(item)
