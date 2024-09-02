# src/views/ui.py

import tkinter as tk
from tkinter import ttk

# from tkinter import font  # Import the font module explicitly
from src.controllers.tree_controller import (
    add_item,
    on_item_select,
    remove_item,
    undo_operation,
)
from src.controllers.drag_handlers import (
    on_drag_start,
    on_drag_motion,
    on_drag_release,
)
from src.models.tree_model import (
    save_treeview,
    load_treeview,
)
from src.views.styles import configure_styles

from src.views.treeview_utils import (
    enable_editing,
    expand_or_collapse_tree,
    load_json_data,
    populate_treeview,
    search_treeview,
)


def generate_context_menu(tree, item, column):
    """Generate a context menu based on the selected item and column."""
    menu = tk.Menu(tree, tearoff=0)

    # Define the actions and their corresponding functions
    actions = {
        "Edit": lambda: enable_editing(tree, item, column),
        "Delete": lambda: remove_item(tree, item),
        # Add more actions here as needed
    }

    for label, command in actions.items():
        menu.add_command(label=label, command=command)

    return menu


def on_right_click(event, tree):
    """Handle the right-click event and show the context menu."""
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return  # Only proceed if the click is within a cell

    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    if item and column:
        # Generate the context menu
        menu = generate_context_menu(tree, item, column)
        # Show the context menu
        menu.post(event.x_root, event.y_root)


def create_treeview(parent, state, logging_text_widget):
    """Create a tree view widget with a hierarchical number column and a vertical scrollbar."""
    # Create a frame to hold the treeview and scrollbar
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a tree view widget with a hierarchical number column.
    # tree = ttk.Treeview(parent, columns=("name", "description"), show="tree headings")
    tree = ttk.Treeview(
        tree_frame,
        columns=("name", "description"),
        show="tree headings",
        yscrollcommand=scrollbar.set,
    )

    # Set up the columns
    tree.heading("#0", text="Number", anchor="w")
    tree.heading("name", text="Name", anchor="w")
    tree.heading("description", text="Description", anchor="w")

    # Configure the columns
    tree.column("#0", width=220, minwidth=220, stretch=False, anchor="w")
    tree.column("name", width=200, anchor="w")
    tree.column("description", width=300, anchor="w")

    tree.pack(fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    scrollbar.config(command=tree.yview)

    # Apply the custom styles
    configure_styles(tree)

    # Bind the selection event
    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: on_item_select(event, state, logging_text_widget),
    )

    # Bind the right-click event
    tree.bind("<Button-3>", lambda event: on_right_click(event, tree))

    tree.update_idletasks()
    return tree


def create_other_tab(notebook, name):
    """Create a generic tab."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=name)

    # Add other UI components as needed for the tab
    # For now, this function creates an empty tab
    return tab


def create_family_standard_tab(notebook, state, logging_text_widget):
    """Create and configure the Family Standard Configuration tab."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="패밀리 표준 구성도")

    # Create a frame for all the buttons (Save, Load, Add, Remove, Undo, Search)
    button_frame = ttk.Frame(tab)
    button_frame.pack(fill=tk.X, pady=10)

    # Create tree view below the buttons
    tree = create_treeview(tab, state, logging_text_widget)

    # Bind dragging events
    tree.bind("<ButtonPress-1>", lambda event: on_drag_start(tree, event))
    tree.bind("<B1-Motion>", lambda event: on_drag_motion(tree, event))
    tree.bind("<ButtonRelease-1>", lambda event: on_drag_release(tree, event))

    # First row: Save, Load, Dropdown, Search box, Search button
    save_button = ttk.Button(
        button_frame, text="Save", command=lambda: save_treeview(tree)
    )
    load_button = ttk.Button(
        button_frame, text="Load", command=lambda: load_treeview(tree)
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
        button_frame, text="Add Item", command=lambda: add_item(tree)
    )
    remove_button = ttk.Button(
        button_frame, text="Remove Item", command=lambda: remove_item(tree)
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
        populate_treeview(tree, json_data)
        tree.update_idletasks()

    # Automatically expand the tree to level 5
    expand_or_collapse_tree(tree, 5)

    # Force a refresh to apply styles
    tree.update_idletasks()
    return tab
