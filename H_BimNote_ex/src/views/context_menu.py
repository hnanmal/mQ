import tkinter as tk

from src.core.treeview_core import remove_item
from src.controllers.treeview.tree_item_manage import edit_tree_item


def generate_context_menu(state, tree, item, column):
    menu = tk.Menu(tree, tearoff=0)
    actions = {
        "Edit": lambda: edit_tree_item(tree, item, column),
        "Delete": lambda: remove_item(tree, state, item),
        # Additional actions...
    }

    for label, command in actions.items():
        menu.add_command(label=label, command=command)

    return menu
