# src/views/project_info_tab/room_treeview_utils.py
import tkinter as tk


def group_inputs(inputs):
    indexes = []
    res = []
    for row_idx, row_input in enumerate(inputs):
        if " / " in row_input:
            indexes.append(row_idx)
    if indexes:
        slice_area = [[x, y] for x, y in zip(indexes[0::1], indexes[1::1])]
        for stt, end in slice_area:
            grp = inputs[stt:end]
            finish_type = grp[0].split("\t")[0]
            room_inputs = grp[1:]
            for room_input in room_inputs:
                room_no, room_name, *_ = room_input.split("\t")
                room_dict = {
                    "room_name": room_name,
                    "room_no": room_no,
                    "finish_type": finish_type,
                }
                res.append(room_dict)
    else:
        for room_input in inputs:
            room_no, room_name, *_ = room_input.split("\t")
            room_dict = {
                "room_name": room_name,
                "room_no": room_no,
                "finish_type": "",
            }
            res.append(room_dict)
    return res


# Function to add items to the Treeview
def add_item_in_roomTree(state, building_treeview, room_treeview, new_room_text):
    selected_building = building_treeview.selection()
    selected_item = room_treeview.selection()
    # state.logging_text_widget.write(f"{selected_building} : {selected_item}")

    new_room_inputs = list(
        filter(lambda x: x != "", new_room_text.get("1.0", "end-1c").split("\n"))
    )
    # state.logging_text_widget.write(f"{new_room_inputs}\n")

    new_rooms = group_inputs(new_room_inputs)

    if selected_building and selected_item:
        # If a parent item is selected, add a child under that item
        parent = selected_item[0]
        room_treeview.insert(
            parent, "end", text=f"Child of {room_treeview.item(parent, 'text')}"
        )
    elif selected_building:
        # If no item is selected, add a new parent item
        for new_room in new_rooms:
            room_treeview.insert(
                "",
                "end",
                text=new_room["room_no"],
                values=(new_room["room_name"], new_room["finish_type"]),
            )
            state.logging_text_widget.write(f"{new_room}\n")
        new_room_text.delete("1.0", tk.END)


# Function to remove selected item
def remove_item_in_roomTree(state, building_treeview, room_treeview):
    selected_item = room_treeview.selection()
    if selected_item:
        room_treeview.delete(selected_item)
