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
