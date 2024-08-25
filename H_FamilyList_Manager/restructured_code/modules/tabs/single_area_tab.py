# single_area_tab.py

import tkinter as tk
from tkinter import ttk, font, filedialog

def create_single_area_tab(app, name):
    # Create a frame for the tab
    main_frame = ttk.Frame(app.notebook)
    main_frame.pack(fill="both", expand=True)

    tab_frame = ttk.Frame(main_frame)
    tab_frame.pack(fill="both", expand=True)

    # Frame for buttons at the top
    button_frame = ttk.Frame(tab_frame)
    button_frame.pack(fill="x", padx=10, pady=10)

    # Frame for buttons at the top
    bottom_frame = ttk.Frame(tab_frame)
    bottom_frame.pack(fill="x", padx=10, pady=10)

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
        button_frame, text="Save", command=lambda: app.config_manager.save_configuration("your_file_path.json")
    )
    save_button.pack(side="left", padx=2, pady=5)

    # Load Button with File Dialog
    def load_config_with_dialog():
        file_path = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        if file_path:
            app.config_manager.load_configuration(file_path)

    # Load Button
    load_button = ttk.Button(
        button_frame, text="Load", command=load_config_with_dialog
    )
    load_button.pack(side="left", padx=2, pady=5)

    # Collapse All Button
    collapse_button = ttk.Button(
        button_frame, text="Collapse All", command=app.treeview_operations.collapse_all
    )
    collapse_button.pack(side="left", padx=2, pady=5)

    # Level limit combobox
    level_limit_var = tk.StringVar()
    app.level_limit_var = level_limit_var
    level_limit_combo = ttk.Combobox(
        button_frame, textvariable=level_limit_var, state="readonly", width=10
    )
    level_limit_combo["values"] = [str(i) for i in range(1, 11)]
    level_limit_combo.current(6)
    level_limit_combo.bind(
        "<<ComboboxSelected>>", app.treeview_operations.update_level_limit
    )
    level_limit_combo.pack(side="left", padx=2, pady=5)

    # Search entry and button
    app.search_var = tk.StringVar()
    app.search_manager.setup_search(button_frame)

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
    app.tree.column("#0", width=50, anchor="center")
    app.tree.column("indented_name", width=300, minwidth=200)
    app.tree.column("description", width=400, minwidth=200)
    app.tree.heading("#0", text="#")
    app.tree.heading("indented_name", text="Item")
    app.tree.heading("description", text="Description")
    app.tree.pack(padx=20, pady=10, fill="both", expand=True)

    # Configure the scrollbar
    tree_scroll.config(command=app.tree.yview)

    # Define custom fonts
    app.font_level_0 = font.Font(family="Arial", size=12, weight="bold")
    app.font_level_4 = font.Font(family="Arial", size=11)
    app.default_font = font.Font(family="Arial", size=9)

    # Define tag for top-level items with light green background and bold font
    app.tree.tag_configure("top_level", background="light green", font=app.font_level_0)
    # Define tag for level 4 items with blue foreground and custom font
    app.tree.tag_configure("level_4", foreground="blue", font=app.font_level_4)

    # Add initial top-level items to the tree
    for i, item in enumerate(app.top_level_items):
        app.treeview_operations.add_numbered_item(
            "", f"{i}", item, "", top_level=True, track_undo=False
        )

    # Bind double-click event for editing item names
    app.tree.bind("<Double-1>", app.treeview_operations.on_item_double_click)

    # Bind single-click event for editing descriptions
    app.tree.bind("<Button-1>", app.treeview_operations.on_item_single_click)

    # Add the tab to the notebook
    app.notebook.add(main_frame, text=f"   {name}   ")

    # Add "Order Adjustment Mode" button
    app.order_adjustment_mode = tk.BooleanVar(value=False)
    app.order_adjustment_button = ttk.Button(
        main_frame,
        text="Order Adjustment Mode: OFF",
        command=app.drag_and_drop_manager.toggle_order_adjustment_mode,
    )
    app.order_adjustment_button.pack(side="bottom", anchor="w", padx=10, pady=5)
