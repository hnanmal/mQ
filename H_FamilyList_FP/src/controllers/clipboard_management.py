# src/controllers/clipboard_management.py

import tkinter as tk

from src.utils.tree_utils import copy_treeview_items, paste_treeview_items

clipboard_data = []

def copy_to_clipboard(tree, selected_items):
    global clipboard_data
    clipboard_data = copy_treeview_items(tree, selected_items)

def paste_from_clipboard(tree, target_item):
    if clipboard_data:
        paste_treeview_items(tree, target_item, clipboard_data)

# def paste_copied_items(destination, clipboard_items):
#     # Example implementation: Append items to the destination list
#     for item in clipboard_items:
#         destination.append(item)
#     print(f"Pasted {len(clipboard_items)} items to destination")

def paste_external_data(tree, target_items, paste_to):
    clipboard_text = tk.Tk().clipboard_get()
    clipboard_lines = clipboard_text.splitlines()

    for i, item in enumerate(target_items):
        if i >= len(clipboard_lines):
            break
        current_values = list(tree.item(item, 'values'))
        if paste_to == 'name':
            current_values[0] = clipboard_lines[i]
        elif paste_to == 'description':
            current_values[1] = clipboard_lines[i]
        tree.item(item, values=tuple(current_values))