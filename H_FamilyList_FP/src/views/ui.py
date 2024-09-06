# src/views/ui.py

import tkinter as tk
from tkinter import ttk

# from tkinter import font  # Import the font module explicitly
from src.core.event_handling import handle_tab_switch
from src.controllers.event_dispatcher import dispatch_event
from src.controllers.tree_controller import (
    add_item,
    remove_item,
    undo_operation,
)
from src.models.tree_model import (
    load_json_data,
    save_treeview,
    load_treeview,
)

# from src.views.styles import configure_styles

from src.views.treeview_utils import (
    expand_or_collapse_tree,
    populate_treeview,
    search_treeview,
)
from src.views.logging_utils import setup_logging_frame
from src.views.treeview_handlers import create_treeview

from src.views.drag_and_drop import (
    on_drag_motion,
)


def handle_tab_click(event, notebook, state):
    """Handle a tab click event."""
    clicked_tab_index = notebook.index("@%d,%d" % (event.x, event.y))
    clicked_tab_name = notebook.tab(clicked_tab_index, "text")

    # Log the clicked tab name
    logging_text_widget = state.logging_text_widget
    # logging_text_widget.write(f"Clicked on tab: {clicked_tab_name}\n")
    logging_text_widget.write(f":: [ {clicked_tab_name} ] 탭에 오셨습니다. ::\n")

    # Set the clicked tab in the state (optional)
    state.set_current_tab(clicked_tab_name)


def create_notebook_with_tabs(root, state):
    main_notebook = ttk.Notebook(root, style="Upper.TNotebook")

    return main_notebook


def create_sub_tab(notebook, name):
    """Create a sub-tab."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=name)
    return tab


def create_team_standard_tab(root, notebook, state):
    """Create the Team Standard tab with its sub-tabs."""
    team_standard_tab = ttk.Frame(notebook)
    notebook.add(team_standard_tab, text="Team Standard")

    team_notebook = ttk.Notebook(
        team_standard_tab, style="Lower.TNotebook"
    )  # Lower-level notebook
    team_notebook.pack(fill="both", expand=True)

    # Add sub-tabs to the "Team Standard" tab
    create_family_standard_tab(root, team_notebook, state)
    create_sub_tab(team_notebook, "WM Group Matching")

    # Bind the tab click event
    team_notebook.bind(
        "<Button-1>", lambda event: handle_tab_click(event, team_notebook, state)
    )


def create_project_standard_tab(notebook, state):
    """Create the Project Standard tab with its sub-tabs."""
    project_standard_tab = ttk.Frame(notebook)
    notebook.add(project_standard_tab, text="Project Standard")  # Use larger tab style

    project_notebook = ttk.Notebook(
        project_standard_tab, style="Lower.TNotebook"
    )  # Lower-level notebook
    project_notebook.pack(fill="both", expand=True)

    other_tab_names = [
        "프로젝트 정보 입력",
        "산출기준",
        "Room",
        "Floors",
        "Roofs",
        "Walls_Ext",
        "Walls_Int",
        "St_Fdn",
        "St_Col",
        "St_Framing",
        "Ceilings",
        "Doors",
        "Windows",
        "Stairs",
        "Railings",
        "Generic",
        "Manual_Input",
    ]

    for name in other_tab_names:
        create_sub_tab(project_notebook, name)

    # Bind the tab click event
    project_notebook.bind(
        "<Button-1>", lambda event: handle_tab_click(event, project_notebook, state)
    )


def create_family_standard_tab(root, notebook, state):
    """Create and configure the Family Standard Configuration tab."""
    tab = create_sub_tab(notebook, "Family Standard Configuration Diagram")
    notebook.add(tab, text="패밀리 표준 구성도")

    # Create a frame for all the buttons (Save, Load, Add, Remove, Undo, Search)
    button_frame = ttk.Frame(tab)
    button_frame.pack(fill=tk.X, pady=10)

    # Create tree view below the buttons
    tree = create_treeview(root, tab, state)

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
        populate_treeview(tree, json_data)
        tree.update_idletasks()

    # Automatically expand the tree to level 5
    expand_or_collapse_tree(tree, 5)

    # Force a refresh to apply styles
    tree.update_idletasks()
    return tab
