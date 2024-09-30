# src/views/tree_management.py

import tkinter as tk
from tkinter import ttk

from src.controllers.tree_controller import add_item, remove_item, undo_operation
from src.models.tree_model import load_json_data, load_treeview, save_treeview
from src.controllers.event_dispatcher import dispatch_event
from src.views.treeview_handlers import create_treeview
from src.views.drag_and_drop import on_drag_motion
from src.views.treeview_utils import (
    expand_or_collapse_tree,
    populate_treeview,
    search_treeview,
)


def create_sub_tab(notebook, name):
    """Create a sub-tab."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=name)
    return tab


def create_family_standard_tab(root, notebook, state):
    """Create and configure the Family Standard Configuration tab."""
    tab = create_sub_tab(notebook, "Family Standard Configuration Diagram")
    notebook.add(tab, text="패밀리 표준 구성도")

    # Create a frame for all the buttons (Save, Load, Add, Remove, Undo, Search)
    button_frame = ttk.Frame(tab)
    button_frame.pack(fill=tk.X, pady=10)

    # Create tree view below the buttons
    tree = create_treeview(tab, state)

    # # Bind dragging events
    tree.bind(
        "<B1-Motion>",
        lambda event: on_drag_motion(tree, event),
    )
    tree.bind(
        "<ButtonPress-1>",
        lambda event: dispatch_event(
            "DRAG_START", state, {"tree": tree, "event": event}
        ),
    )
    tree.bind(
        "<ButtonRelease-1>",
        lambda event: dispatch_event(
            "DRAG_RELEASE", state, {"tree": tree, "event": event}
        ),
    )

    # First row: Save, Load, Dropdown, Search box, Search button
    save_button = ttk.Button(
        button_frame, text="Save", command=lambda: save_treeview(state, tree)
    )
    load_button = ttk.Button(
        button_frame, text="Load", command=lambda: load_treeview(state, tree)
    )

    level_options = list(range(1, 11))  # Define levels to expand/collapse
    combobox = ttk.Combobox(button_frame, values=level_options, state="readonly")
    combobox.set(5)
    combobox.bind(
        "<<ComboboxSelected>>",
        lambda event: expand_or_collapse_tree(tree, int(combobox.get())),
    )

    search_var = tk.StringVar()  # Variable for search input
    search_entry = ttk.Entry(button_frame, textvariable=search_var)
    search_button = ttk.Button(
        button_frame,
        text="Search",
        command=lambda: search_treeview(tree, search_var.get()),
    )

    # Bind Enter key to the search function
    search_entry.bind("<Return>", lambda event: search_treeview(tree, search_var.get()))

    save_button.grid(row=0, column=0, padx=5, pady=5)
    load_button.grid(row=0, column=1, padx=5, pady=5)
    combobox.grid(row=0, column=2, padx=5, pady=5)
    search_entry.grid(row=0, column=3, padx=5, pady=5)
    search_button.grid(row=0, column=4, padx=5, pady=5)

    # Second row: Add Item, Remove Item, and Undo buttons
    add_button = ttk.Button(
        button_frame, text="Add Item", command=lambda: add_item(tree, state)
    )
    remove_button = ttk.Button(
        button_frame, text="Remove Item", command=lambda: remove_item(tree, state)
    )
    undo_button = ttk.Button(
        button_frame, text="Undo", command=lambda: undo_operation(tree)
    )

    add_button.grid(row=1, column=0, padx=5, pady=5)
    remove_button.grid(row=1, column=1, padx=5, pady=5)
    undo_button.grid(row=1, column=2, padx=5, pady=5)

    # Load the JSON data and populate the tree view
    json_file_path = "resources/defaultTypeTree.json"
    json_data = load_json_data(json_file_path)
    if json_data:
        ## state 에 defaultTree 저장
        state.stdTypes_info = json_data

        populate_treeview(tree, json_data)
        tree.update_idletasks()

    # Automatically expand the tree to level 5
    expand_or_collapse_tree(tree, 5)

    # Force a refresh to apply styles
    tree.update_idletasks()
    return tab
