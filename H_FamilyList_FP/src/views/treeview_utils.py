# src/views/treeview_utils.py

import json
import os
import tkinter as tk
from tkinter import filedialog

from src.controllers.tree_controller import *
from src.views.styles import configure_styles


def get_clicked_column(tree, event):
    """Determine which column was clicked based on x-coordinate."""
    return tree.identify_column(event.x)


def enable_editing(tree, item, column):
    """Enable editing for the specified column of the treeview item."""
    x, y, width, height = tree.bbox(item, column)
    entry = tk.Entry(tree, width=width)

    # Get the current text in the cell
    current_value = tree.item(item, "values")[int(column[1:]) - 1]

    entry.insert(0, current_value)
    entry.place(x=x, y=y, width=width, height=height)

    def save_edit(event):
        new_value = entry.get()
        tree.set(item, column=column, value=new_value)
        entry.destroy()

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", lambda event: entry.destroy())
    entry.focus()


search_state = {"last_search": None, "last_match": None}


def search_treeview(tree, search_text):
    """Search the Treeview for items that match the search_text in the Name or Description."""
    global search_state
    items = tree.get_children("")

    # Flatten the tree to get a list of all items
    all_items = []

    def flatten_tree(parent):
        for item in tree.get_children(parent):
            all_items.append(item)
            flatten_tree(item)

    flatten_tree("")

    # If continuing from the last search, start after the last matched item
    start_index = 0
    if (
        search_state["last_search"] == search_text
        and search_state["last_match"] is not None
    ):
        start_index = all_items.index(search_state["last_match"]) + 1

    # Search for the next match
    for i in range(start_index, len(all_items)):
        item = all_items[i]
        item_values = tree.item(item, "values")
        item_name = item_values[0] if len(item_values) > 0 else ""
        item_description = item_values[1] if len(item_values) > 1 else ""

        if (
            search_text.lower() in item_name.lower()
            or search_text.lower() in item_description.lower()
        ):
            tree.selection_set(item)
            tree.see(item)
            search_state["last_search"] = search_text
            search_state["last_match"] = item
            return

    # If no match is found or the end of the tree is reached, reset the search
    search_state["last_search"] = None
    search_state["last_match"] = None
    print("No more matches found.")


def load_json_data(file_path):
    """Load JSON data from a file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print("JSON data loaded successfully.")
            return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        return None


def save_json_data(file_path, data):
    """Save data to a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print("Tree view data saved successfully.")
    except Exception as e:
        print(f"Error saving JSON: {e}")


def populate_treeview(tree, data, parent="", level=0):
    """Populate the Treeview widget with JSON data."""

    def insert_items(parent, items, level):
        for item in items:
            # Determine the appropriate tag based on the level
            tag = determine_tag_by_level(level)

            # Add indentation based on the level
            indented_name = "  " * level + item["name"]
            node_id = tree.insert(
                parent,
                "end",
                text=item["number"],
                values=(indented_name, item.get("description", "")),
                tags=(tag,),
            )
            children = item.get("children", [])
            if children:
                insert_items(node_id, children, level + 1)

    tree.delete(*tree.get_children())  # Clear the existing tree view
    insert_items(parent, data, level)

    # Force a refresh to apply styles
    configure_styles(tree)
    tree.update_idletasks()


def expand_or_collapse_tree(tree, level):
    """Expand or collapse tree view items up to the specified level."""

    def expand_children(item, current_level, target_level):
        if current_level < target_level:
            tree.item(item, open=True)
            children = tree.get_children(item)
            for child in children:
                expand_children(child, current_level + 1, target_level)
        else:
            tree.item(item, open=False)

    root_items = tree.get_children("")
    for item in root_items:
        expand_children(item, 1, level)

    configure_styles(tree)
    tree.update_idletasks()
