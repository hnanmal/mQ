# Version: 1.0.12

import tkinter as tk
from tkinter import ttk, font
from search import SearchManager


def create_single_area_tab(app, name):
    # Create a frame for the tab
    tab_frame = ttk.Frame(app.notebook)
    tab_frame.pack(fill="both", expand=True)

    # Frame for buttons at the top
    button_frame = ttk.Frame(tab_frame)
    button_frame.pack(fill="x", padx=10, pady=10)

    # Add Item Button
    add_button = ttk.Button(
        button_frame, text="Add Item", command=app.treeview_operations.add_item
    )
    add_button.pack(side="left", padx=2, pady=5)

    # Remove Selected Button
    remove_button = ttk.Button(
        button_frame,
        text="Remove Selected",
        command=app.treeview_operations.remove_selected_item,
    )
    remove_button.pack(side="left", padx=2, pady=5)

    # Save Button
    save_button = ttk.Button(
        button_frame, text="Save", command=app.config_manager.save_configuration
    )
    save_button.pack(side="left", padx=2, pady=5)

    # Load Button
    load_button = ttk.Button(
        button_frame, text="Load", command=app.config_manager.load_configuration
    )
    load_button.pack(side="left", padx=2, pady=5)

    # Collapse All Button
    collapse_button = ttk.Button(
        button_frame, text="Collapse All", command=app.treeview_operations.collapse_all
    )
    collapse_button.pack(side="left", padx=2, pady=5)

    # Level limit combobox
    level_limit_var = tk.StringVar()  # Corrected to use tk.StringVar() directly
    app.level_limit_var = level_limit_var  # Save to the app instance
    level_limit_combo = ttk.Combobox(
        button_frame, textvariable=level_limit_var, state="readonly", width=10
    )
    level_limit_combo["values"] = [str(i) for i in range(1, 11)]  # Levels 1 to 10
    level_limit_combo.current(2)  # Default to level 3
    level_limit_combo.bind(
        "<<ComboboxSelected>>", app.treeview_operations.update_level_limit
    )
    level_limit_combo.pack(side="left", padx=2, pady=5)

    # Search entry and button (added back from v1.4.4)
    app.search_var = tk.StringVar()
    app.search_manager.setup_search(button_frame) ### mk
    # search_entry = ttk.Entry(button_frame, textvariable=app.search_var, width=30)
    # search_entry.bind("<Return>", app.search_manager.on_enter_key)
    # search_button = ttk.Button(
    #     button_frame, text="Search", command=app.search_manager.search_items
    # )
    # search_entry.pack(side="right", padx=2, pady=5)
    # search_button.pack(side="right", padx=2, pady=5)

    # Create a frame for the treeview and scrollbar
    tree_frame = ttk.Frame(tab_frame)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a vertical scrollbar and associate it with the treeview
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    # Create and pack the Treeview widget inside this frame
    app.tree = ttk.Treeview(
        tree_frame,
        columns=("indented_name", "description"),
        show="tree headings",
        yscrollcommand=tree_scroll.set,
        style="Treeview",
    )
    app.tree.column("#0", width=50, anchor="center")  # Tree structure column
    app.tree.column("indented_name", width=300, minwidth=200)
    app.tree.column("description", width=400, minwidth=200)
    app.tree.heading("#0", text="#")
    app.tree.heading("indented_name", text="Item")
    app.tree.heading("description", text="Description")
    app.tree.pack(padx=20, pady=10, fill="both", expand=True)

    # Configure the scrollbar
    tree_scroll.config(command=app.tree.yview)

    # Define custom fonts
    app.font_level_0 = font.Font(family="Arial", size=14, weight="bold")
    app.font_level_4 = font.Font(family="Arial", size=12)
    app.default_font = font.Font(family="Arial", size=10)

    # Define tag for top-level items with light green background and bold font
    app.tree.tag_configure("top_level", background="light green", font=app.font_level_0)
    # Define tag for level 4 items with blue foreground and custom font
    app.tree.tag_configure("level_4", foreground="blue", font=app.font_level_4)

    # Add initial top-level items to the tree
    for i, item in enumerate(app.top_level_items):
        app.treeview_operations.add_numbered_item("", f"{i}", item, "", top_level=True)

    # Bind double-click event for editing item names
    app.tree.bind("<Double-1>", app.treeview_operations.on_item_double_click)

    # Bind single-click event for editing descriptions
    app.tree.bind("<Button-1>", app.treeview_operations.on_item_single_click)

    # Add the tab to the notebook
    app.notebook.add(tab_frame, text=f"   {name}   ")


def create_three_area_tab(app, name):
    # Create a frame for the tab
    tab_frame = ttk.Frame(app.notebook)

    # Create left, middle, and right frames
    left_frame = ttk.Frame(tab_frame)
    middle_frame = ttk.Frame(tab_frame)
    right_frame = ttk.Frame(tab_frame)

    # Left content
    left_label = ttk.Label(left_frame, text=f"Left content of {name}")
    left_button = ttk.Button(
        left_frame,
        text="Left Button",
        command=lambda: app.context_menu_manager.on_button_click(
            f"Left Button on {name}"
        ),
    )
    left_text = ttk.Entry(left_frame, width=30)

    # Middle content
    middle_label = ttk.Label(middle_frame, text=f"Middle content of {name}")
    middle_button = ttk.Button(
        middle_frame,
        text="Middle Button",
        command=lambda: app.context_menu_manager.on_button_click(
            f"Middle Button on {name}"
        ),
    )
    middle_text = ttk.Entry(middle_frame, width=30)

    # Right content
    right_label = ttk.Label(right_frame, text=f"Right content of {name}")
    right_button = ttk.Button(
        right_frame,
        text="Right Button",
        command=lambda: app.context_menu_manager.on_button_click(
            f"Right Button on {name}"
        ),
    )
    right_text = ttk.Entry(right_frame, width=30)

    # Pack left content with padding
    left_label.pack(padx=20, pady=10)
    left_button.pack(padx=20, pady=10)
    left_text.pack(padx=20, pady=10)

    # Pack middle content with padding
    middle_label.pack(padx=20, pady=10)
    middle_button.pack(padx=20, pady=10)
    middle_text.pack(padx=20, pady=10)

    # Pack right content with padding
    right_label.pack(padx=20, pady=10)
    right_button.pack(padx=20, pady=10)
    right_text.pack(padx=20, pady=10)

    # Layout left, middle, and right frames
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    middle_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Add the tab to the notebook with increased padding
    app.notebook.add(tab_frame, text=f"   {name}   ")
