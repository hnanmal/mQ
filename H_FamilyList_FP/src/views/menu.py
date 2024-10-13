# src/views/menus.py

import tkinter as tk
from src.controllers.tree_controller import remove_item
from src.utils.tree_utils import enable_tree_item_editing


def generate_context_menu(state, tree, item, column):
    menu = tk.Menu(tree, tearoff=0)
    actions = {
        "Edit": lambda: enable_tree_item_editing(tree, item, column),
        "Delete": lambda: remove_item(tree, state, item),
        # Additional actions...
    }

    for label, command in actions.items():
        menu.add_command(label=label, command=command)

    return menu
