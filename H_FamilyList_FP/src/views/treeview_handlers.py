# src/views/treeview_handlers.py

import tkinter as tk
from tkinter import ttk
from src.controllers.tree_controller import on_item_select
from src.views.menu import generate_context_menu
from src.views.styles import configure_styles
from src.controllers.clipboard_management import (
    copy_to_clipboard,
    paste_from_clipboard,
    paste_external_data,
)
# from src.controllers.clipboard_management import clipboard_data  # Ensure this is imported
clipboard_data = None

def create_treeview(root, parent, state, logging_text_widget):
    """Create a tree view widget with a hierarchical number column and a vertical scrollbar."""
    # Create a frame to hold the treeview and scrollbar
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a tree view widget with a hierarchical number column.
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

    tree.bind("<Control-c>", lambda e: handle_copy(root, tree, e))
    tree.bind("<Control-v>", lambda e: handle_paste(tree, e, clipboard_data))

    # tree.update_idletasks()
    return tree

def on_right_click(event, tree):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if item and column:
        menu = generate_context_menu(tree, item, column)
        menu.post(event.x_root, event.y_root)

def handle_copy(root, tree, event):
    if root.focus_get() == tree:
        print("Copy event triggered")
    else:
        print("Treeview is not focused")


# def handle_copy(tree, event):
#     global clipboard_data
#     try:
#         selected_items = tree.selection()
#         if selected_items:
#             copy_to_clipboard(tree, selected_items)
#             print(f"{selected_items} copied!")
#     except Exception as e:
#         print(f"Error during copy: {e}")

def handle_paste(tree, event,):# clipboard_data):
    global clipboard_data
    try:
        selected_items = tree.selection()
        if selected_items:
            # Paste within tree view if items were copied within the tree
            if clipboard_data:
                paste_from_clipboard(tree, selected_items[0])
            else:
                # Handle pasting text data from external sources
                paste_target_items = selected_items
                paste_to = ask_paste_location()
                if paste_to:
                    paste_external_data(tree, paste_target_items, paste_to)
    except Exception as e:
        print(f"Error during paste: {e}")

def ask_paste_location():
    """Prompt user to select whether to paste into Name or Description."""
    paste_dialog = tk.Tk()
    paste_dialog.withdraw()  # Hide the root window

    result = tk.messagebox.askquestion(
        "Paste Location",
        "Where do you want to paste the text?",
        icon='question',
        type='radio',
        options=['name', 'description'],
    )

    paste_dialog.destroy()
    return result
