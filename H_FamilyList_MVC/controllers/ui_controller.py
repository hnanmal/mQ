import tkinter as tk
from openpyxl import load_workbook
from models.wm_group import (
    load_wm_group_match_data,
    save_lock_status_to_json,
    save_current_matching_to_json,
    filter_excel_data,
    save_configuration,
    load_configuration,
)


def get_item_texts(item_values):
    res = [
        item_values[0],
        item_values[3],
        item_values[5],
        item_values[7],
        item_values[9],
        item_values[11],
        item_values[13],
        item_values[15],
        item_values[17],
        item_values[19],
        item_values[21],
        item_values[23],
    ]
    return res


def add_item_to_center(app):
    selected_items = app.excel_treeview.selection()
    if not selected_items:
        tk.messagebox.showwarning(
            "No Selection", "Please select an item from the Excel data."
        )
        return

    for item in selected_items:
        item_values = app.excel_treeview.item(item, "values")
        # Get the 0th, 7th, and 9th column values
        item_texts = get_item_texts(item_values)
        item_string = " - ".join(item_texts)

        # Insert all selected values into the Listbox
        app.drop_area.insert(
            tk.END,
            item_string,
        )  # Insert item text into the Listbox


def remove_item_from_center(app):
    selected_index = app.drop_area.curselection()
    if selected_index:
        app.drop_area.delete(selected_index)


def toggle_lock(app, add_button, remove_button, lock_button):
    # Get the currently selected item
    selected_item = app.wm_group_treeview.selection()
    if not selected_item:
        return

    item_name = app.wm_group_treeview.item(selected_item[0], "values")[0]

    # Toggle the lock state for the current item
    is_locked = app.lock_status.get(item_name, False)
    app.lock_status[item_name] = not is_locked

    # Update the lock button text
    lock_button.config(text="Unlock" if app.lock_status[item_name] else "Lock")

    # Update the background color of the drop area based on the lock state
    app.drop_area.config(bg="gray" if app.lock_status[item_name] else "white")

    # Update the treeview item color based on the lock state
    if app.lock_status[item_name]:
        app.wm_group_treeview.item(selected_item[0], tags=("locked",))
    else:
        app.wm_group_treeview.item(selected_item[0], tags=("unlocked",))

    # Save the current matching results to JSON
    save_current_matching_to_json(app, item_name)

    # Save the lock status to wm_group_match.json
    save_lock_status_to_json(app)

    # Update the item color in the left area
    app.wm_group_treeview.item(
        selected_item, tags=("locked" if app.lock_status[item_name] else "unlocked")
    )
