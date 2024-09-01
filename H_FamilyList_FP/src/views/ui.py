# src/views/ui.py

import tkinter as tk
from tkinter import ttk
from tkinter import font  # Import the font module explicitly
from src.views.styles import configure_styles
from src.views.treeview_utils import (
    save_treeview, 
    load_treeview, 
    expand_or_collapse_tree,
    load_json_data,
    populate_treeview,
    add_item,
    remove_item,
    undo_operation,
    search_treeview,
)

def on_item_select(event, tree, logging_text_widget):
    """Handle the selection of an item in the Treeview."""
    selected_item = tree.selection()[0]  # Get the ID of the selected item
    item_values = tree.item(selected_item, 'values')  # Get the item's values
    item_number = tree.item(selected_item, 'text')  # Get the item's number

    # Extract the relevant information
    name = item_values[0] if len(item_values) > 0 else "No Name"
    description = item_values[1] if len(item_values) > 1 else "No Description"

    # Prepare the log message
    log_message = f"Selected Item:\nNumber: {item_number}\nName: {name}\nDescription: {description}\n"

    # Write the information to the logging area
    logging_text_widget.write(log_message)

def create_treeview(parent, logging_text_widget):
    """Create a tree view widget with a hierarchical number column."""
    tree = ttk.Treeview(parent, columns=("name", "description"), show="tree headings")

    # Set up the columns
    tree.heading("#0", text="Number", anchor="w")
    tree.heading("name", text="Name", anchor="w")
    tree.heading("description", text="Description", anchor="w")

    # Configure the columns
    tree.column("#0", width=220, minwidth=220, stretch=False, anchor="w")
    tree.column("name", width=200, anchor="w")
    tree.column("description", width=300, anchor="w")

    tree.pack(fill=tk.BOTH, expand=True)

    # Apply the custom styles
    configure_styles(tree)

    # Bind the selection event
    tree.bind("<<TreeviewSelect>>", lambda event: on_item_select(event, tree, logging_text_widget))

    return tree

def create_buttons(parent, save_command, load_command):
    """Create Save and Load buttons."""
    button_frame = ttk.Frame(parent)
    button_frame.pack(fill=tk.X, pady=10)

    save_button = ttk.Button(button_frame, text="Save", command=save_command)
    load_button = ttk.Button(button_frame, text="Load", command=load_command)

    save_button.pack(side=tk.LEFT, padx=5)
    load_button.pack(side=tk.LEFT, padx=5)

    return button_frame

def create_other_tab(notebook, name):
    """Create a generic tab."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=name)

    # Add other UI components as needed for the tab
    # For now, this function creates an empty tab
    return tab

# def create_family_standard_tab(notebook, state, logging_text_widget):
#     """Create and configure the Family Standard Configuration tab."""
#     tab = ttk.Frame(notebook)
#     notebook.add(tab, text="패밀리 표준 구성도")

#     # Create a frame for all the buttons (Save, Load, Add, Remove, Undo)
#     button_frame = ttk.Frame(tab)
#     button_frame.pack(fill=tk.X, pady=10)

#     # Create tree view below the buttons
#     tree = create_treeview(tab, logging_text_widget)

#     # First row: Save, Load, and Dropdown buttons
#     save_button = ttk.Button(button_frame, text="Save", command=lambda: save_treeview(tree))
#     load_button = ttk.Button(button_frame, text="Load", command=lambda: load_treeview(tree))
    
#     level_options = list(range(1, 11))  # Define levels to expand/collapse
#     combobox = ttk.Combobox(button_frame, values=level_options, state="readonly")
    
#     # Set combo box to level 5, matching the initial expansion level
#     combobox.set(5)
    
#     combobox.bind("<<ComboboxSelected>>", lambda event: expand_or_collapse_tree(tree, int(combobox.get())))

#     save_button.grid(row=0, column=0, padx=5, pady=5)
#     load_button.grid(row=0, column=1, padx=5, pady=5)
#     combobox.grid(row=0, column=2, padx=5, pady=5)

#     # Second row: Add Item, Remove Item, and Undo buttons
#     add_button = ttk.Button(button_frame, text="Add Item", command=lambda: add_item(tree))
#     remove_button = ttk.Button(button_frame, text="Remove Item", command=lambda: remove_item(tree))
#     undo_button = ttk.Button(button_frame, text="Undo", command=lambda: undo_operation(tree))

#     add_button.grid(row=1, column=0, padx=5, pady=5)
#     remove_button.grid(row=1, column=1, padx=5, pady=5)
#     undo_button.grid(row=1, column=2, padx=5, pady=5)

#     # Load the JSON data and populate the tree view
#     json_file_path = "resources/defaultTypeTree.json"
#     json_data = load_json_data(json_file_path)
#     if json_data:
#         populate_treeview(tree, json_data)

#     # Ensure styles are applied after the tree is populated
#     configure_styles(tree)

#     # Automatically expand the tree to level 5
#     expand_or_collapse_tree(tree, 5)
    
#     # Force a refresh to apply styles
#     tree.update_idletasks()

#     return tab

def create_family_standard_tab(notebook, state, logging_text_widget):
    """Create and configure the Family Standard Configuration tab."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="패밀리 표준 구성도")

    # Create a frame for all the buttons (Save, Load, Add, Remove, Undo, Search)
    button_frame = ttk.Frame(tab)
    button_frame.pack(fill=tk.X, pady=10)

    # Create tree view below the buttons
    tree = create_treeview(tab, logging_text_widget)

    # First row: Save, Load, Dropdown, Search box, Search button
    save_button = ttk.Button(button_frame, text="Save", command=lambda: save_treeview(tree))
    load_button = ttk.Button(button_frame, text="Load", command=lambda: load_treeview(tree))
    
    level_options = list(range(1, 11))  # Define levels to expand/collapse
    combobox = ttk.Combobox(button_frame, values=level_options, state="readonly")
    combobox.set(5)
    combobox.bind("<<ComboboxSelected>>", lambda event: expand_or_collapse_tree(tree, int(combobox.get())))

    search_var = tk.StringVar()  # Variable for search input
    search_entry = ttk.Entry(button_frame, textvariable=search_var)
    search_button = ttk.Button(button_frame, text="Search", command=lambda: search_treeview(tree, search_var.get()))

    # Bind Enter key to the search function
    search_entry.bind("<Return>", lambda event: search_treeview(tree, search_var.get()))

    save_button.grid(row=0, column=0, padx=5, pady=5)
    load_button.grid(row=0, column=1, padx=5, pady=5)
    combobox.grid(row=0, column=2, padx=5, pady=5)
    search_entry.grid(row=0, column=3, padx=5, pady=5)
    search_button.grid(row=0, column=4, padx=5, pady=5)

    # Second row: Add Item, Remove Item, and Undo buttons
    add_button = ttk.Button(button_frame, text="Add Item", command=lambda: add_item(tree))
    remove_button = ttk.Button(button_frame, text="Remove Item", command=lambda: remove_item(tree))
    undo_button = ttk.Button(button_frame, text="Undo", command=lambda: undo_operation(tree))

    add_button.grid(row=1, column=0, padx=5, pady=5)
    remove_button.grid(row=1, column=1, padx=5, pady=5)
    undo_button.grid(row=1, column=2, padx=5, pady=5)

    # Load the JSON data and populate the tree view
    json_file_path = "resources/defaultTypeTree.json"
    json_data = load_json_data(json_file_path)
    if json_data:
        populate_treeview(tree, json_data)

    # Automatically expand the tree to level 5
    expand_or_collapse_tree(tree, 5)
    
    # Force a refresh to apply styles
    tree.update_idletasks()
    return tab
