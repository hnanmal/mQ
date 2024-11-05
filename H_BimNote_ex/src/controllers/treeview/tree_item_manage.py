from copy import deepcopy
import tkinter as tk

# from src.controllers.event_controllers import dispatch_event


def edit_tree_item(tree, item, column):  # 구 enable_tree_item_editing
    """Enable editing for the specified column of the treeview item."""
    x, y, width, height = tree.bbox(item, column)
    entry = tk.Entry(tree, width=width)

    # Get the current text in the cell
    current_value = tree.item(item, "values")[int(column[1:]) - 1]

    entry.insert(0, current_value)
    entry.place(x=x, y=y, width=width, height=height)

    def save_edit(event):
        new_value = entry.get()
        tree.set(item, column=column, value=new_value)
        entry.destroy()

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", lambda event: entry.destroy())
    # entry.bind("<FocusOut>", lambda event: save_edit)
    entry.focus()
