import tkinter as tk
from tkinter import ttk

from src.controllers.treeview.treeview_controllers import (
    handle_copy,
    handle_paste,
    on_item_select,
    on_right_click,
)
from src.views.styles import configure_tree_styles

# from src.controllers.treeview.tree_item_manage import renumber_treeview_items


def create_treeview(parent, state, heads=None):
    """Create a tree view widget with a hierarchical number column and a vertical scrollbar."""

    # Function to scroll to the selected item when the spacebar is pressed
    def scroll_to_selected_item(event, tree):
        selected_item = tree.selection()
        if selected_item:
            tree.see(selected_item[0])  # Ensure the selected item is visible

    # Create a frame to hold the treeview and scrollbar
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create horizontal scrollbar
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a tree view widget with a hierarchical number column.

    if heads:
        tree = ttk.Treeview(
            tree_frame,
            columns=heads,
            show="tree headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scroll.set,
        )
        for idx, head in enumerate(heads):
            # tree.heading(idx, text=head, anchor="w")
            if idx == 0:
                pass
            else:
                tree.heading(idx, text=head, anchor="w")
    else:
        tree = ttk.Treeview(
            tree_frame,
            columns=("name", "description"),
            show="tree headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scroll.set,
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
    v_scrollbar.config(command=tree.yview)

    # Apply the custom styles
    configure_tree_styles(tree)

    # Bind the selection event
    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: on_item_select(event, state),
    )

    tree.bind("<space>", lambda e: scroll_to_selected_item(e, tree))

    # Bind the right-click event
    tree.bind("<Button-3>", lambda event: on_right_click(event, state, tree))

    tree.bind("<Control-c>", lambda event: handle_copy(tree, event, state))
    tree.bind("<Control-v>", lambda event: handle_paste(tree, event, state))

    tree.update_idletasks()
    return tree
