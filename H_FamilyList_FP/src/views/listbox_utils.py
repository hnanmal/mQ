# src/views/listbox_utils.py

import tkinter as tk
from tkinter import ttk
from tksheet.other_classes import Box_nt

from src.models.tree_model import load_json_data


def collect_level_6_items(tree_data, level=0, current_items=None):
    """Recursively collect items that are at level 6."""
    if current_items is None:
        current_items = []

    for item in tree_data:
        if level == 6 and item["name"] not in current_items:
            current_items.append(item["name"])
        if "children" in item and item["children"]:
            collect_level_6_items(item["children"], level + 1, current_items)

    return current_items


def get_selected_row_indices(sheet_widget):
    """Extract only the indices of the selected rows from tksheet."""
    selected_items = sheet_widget.get_currently_selected()

    # Debug: print the selected items and their types
    print(f"Selected items: {selected_items}")
    print(f"Types of selected items: {[type(item) for item in selected_items]}")

    selected_rows = set()  # Use a set to avoid duplicates

    # Iterate over all selected items
    for item in selected_items:
        # Handle range selections via Box_nt
        if isinstance(item, Box_nt):
            selected_rows.update(
                range(item.from_r, item.upto_r)
            )  # Add the range of row indices
    # Return the sorted list of selected row indices
    return sorted(selected_rows)


def add_selected_row_to_listbox(sheet_widget, listbox):
    """Add the selected row(s) from the Excel sheet to the listbox in section2."""
    if sheet_widget is not None:
        selected_items = sheet_widget.get_currently_selected()

        # Debug: print the selected items and their types
        print(f"Selected items: {selected_items}")
        print(f"Types of selected items: {[type(item) for item in selected_items]}")

        row_indexs = get_selected_row_indices(sheet_widget)
        # Add the valid rows to the listbox, avoiding duplicates
        for row_index in row_indexs:
            try:
                row_data = sheet_widget.get_row_data(row_index)
                print(type(row_data))
                if row_data:
                    str_row_data = list(map(str, row_data))
                    # listbox.insert(tk.END, f"Row {row_index}: {row_data}")
                    listbox.insert(tk.END, "... | ...".join(str_row_data))
            except (ValueError, TypeError) as e:
                print(f"Error processing row {row_index}: {e}")


def remove_selected_items_from_listbox(listbox):
    """Remove selected items from the center listbox."""
    selected_items = listbox.curselection()
    for item in reversed(selected_items):  # Reverse to avoid indexing issues
        listbox.delete(item)


def display_level_6_items_list(parent, on_select_item):
    """Display level 6 items from defaultTypeTree.json in a Listbox with a scrollbar."""
    file_path = "resources/defaultTypeTree.json"
    tree_data = load_json_data(file_path)

    if tree_data:
        level_6_items = collect_level_6_items(tree_data)

        # Create a frame to hold the Listbox and scrollbar
        listbox_frame = ttk.Frame(parent)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the Listbox and attach the scrollbar
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Add level 6 items to the Listbox
        for item in level_6_items:
            listbox.insert(tk.END, item)

        # Bind the selection event
        def on_listbox_select(event):
            selected_index = listbox.curselection()
            if selected_index:
                selected_item = listbox.get(selected_index)
                on_select_item(selected_item)

        listbox.bind("<<ListboxSelect>>", on_listbox_select)
        # Force a refresh to apply styles immediately
        listbox.update_idletasks()

        return listbox  # Return the listbox widget
