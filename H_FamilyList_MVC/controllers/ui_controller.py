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

# import logging

# # Configure logging to write to a file
# logging.basicConfig(
#     filename="debug_log.txt",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )


def check_used_wm_item(app):
    # logging.debug("Starting check_used_wm_item function")

    """Highlight Excel rows that match any item in wm_group_match_data based on substring matching with the first item."""
    # Get the matched items from wm_group_match.json
    matched_items = set()
    for group, items in app.wm_group_match_data.items():
        matched_items.update(items)
    # logging.debug(f"Matched items: {matched_items}")

    # Define a tag for blue text color and light gray background
    app.excel_treeview.tag_configure(
        "highlight", foreground="blue", background="light gray"
    )
    # logging.debug("Highlight tag configured in Treeview")

    # Iterate over all rows in the Excel Treeview
    for row_id in app.excel_treeview.get_children():
        row_data = app.excel_treeview.item(row_id, "values")
        # logging.debug(f"Row data: {row_data}")

        # Check if the first item in the row is a substring of any item in wm_group_match_data
        first_item = str(row_data[0]).strip() if row_data else ""
        if any(first_item in matched_item for matched_item in matched_items):
            app.excel_treeview.item(row_id, tags=("highlight",))
            # logging.debug(f"Applied highlight tag to row: {row_data}")
        else:
            app.excel_treeview.item(row_id, tags=())
            # logging.debug(f"No match for row: {row_data}")

    app.excel_treeview.update_idletasks()


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
        item_string = " |: ".join(item_texts)

        # Insert all selected values into the Listbox
        app.drop_area.insert(
            tk.END,
            item_string,
        )  # Insert item text into the Listbox


def remove_item_from_center(app):
    selected_index = app.drop_area.curselection()
    if selected_index:
        app.drop_area.delete(selected_index)


def update_drop_area(app, item_name):
    # Clear the current content in the center area
    app.drop_area.delete(0, tk.END)

    # Check if there is matching data in wm_group_match_data
    if item_name in app.wm_group_match_data:
        # Populate the center area with the matched data
        for entry in app.wm_group_match_data[item_name]:
            app.drop_area.insert(tk.END, entry)
    else:
        # If no match is found, leave the area empty or display a placeholder
        app.drop_area.insert(tk.END, "No matching data found.")


def toggle_lock(app, add_button, remove_button, lock_button):
    # Determine the current state
    is_locked = lock_button.config("text")[-1] == "Lock"  #####

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
        # Disable the + and - buttons when locked
        add_button.config(state=tk.DISABLED)
        remove_button.config(state=tk.DISABLED)
    else:
        app.wm_group_treeview.item(selected_item[0], tags=("unlocked",))
        # Enable the + and - buttons when unlocked
        add_button.config(state=tk.NORMAL)
        remove_button.config(state=tk.NORMAL)

    # Save the current matching results to JSON
    save_current_matching_to_json(app, item_name)

    # Save the lock status to wm_group_match.json
    save_lock_status_to_json(app)

    # Update the drop area content after toggling the lock
    update_drop_area(app, item_name)
    # Update the item color in the left area
    app.wm_group_treeview.item(
        selected_item, tags=("locked" if app.lock_status[item_name] else "unlocked")
    )
