import tkinter as tk
from tkinter import ttk
import json


def on_item_double_click(app, event):
    selected_item = app.tree.identify_row(event.y)
    column = app.tree.identify_column(event.x)
    if column == "#1":
        edit_item_name(app, selected_item)


def edit_item_name(app, item):
    current_value = app.original_names.get(item, "")

    app.is_text_editing = True

    entry = ttk.Entry(app.tree, width=len(current_value) + 5)
    entry.insert(0, current_value)
    entry.bind("<Return>", lambda e: save_item_name(app, entry, item))
    entry.bind("<FocusOut>", lambda e: save_item_name(app, entry, item))
    bbox = app.tree.bbox(item, column="indented_name")
    if bbox:
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        entry.focus()
    else:
        entry.destroy()


def save_item_name(app, entry, item):
    try:
        new_value = entry.get()
        app.original_names[item] = new_value
        app.treeview_operations.update_displayed_name(item)
    except tk.TclError:
        pass
    finally:
        app.is_text_editing = False
        entry.destroy()


def on_item_single_click(app, event):
    selected_item = app.tree.identify_row(event.y)
    column = app.tree.identify_column(event.x)
    if column == "#2":  # "#2" corresponds to the Description column
        edit_description(app, selected_item)


def edit_description(app, item):
    current_value = app.tree.set(item, "description")

    app.is_text_editing = True

    entry = ttk.Entry(app.tree, width=len(current_value) + 5)
    entry.insert(0, current_value)
    entry.bind("<Return>", lambda e: save_description(app, entry, item))
    entry.bind("<FocusOut>", lambda e: save_description(app, entry, item))
    bbox = app.tree.bbox(item, column="description")
    if bbox:
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        entry.focus()
    else:
        entry.destroy()


def save_description(app, entry, item):
    try:
        new_value = entry.get()
        app.tree.set(item, "description", new_value)
    except tk.TclError:
        pass
    finally:
        app.is_text_editing = False
        entry.destroy()


def update_center_title_label(app, event):
    selected_item = app.wm_group_treeview.selection()

    if selected_item:
        item_name = app.wm_group_treeview.item(selected_item[0], "values")[0]
        app.center_title_label.config(text=item_name)
        app.drop_area.delete(0, tk.END)

        if item_name in app.wm_group_match_data:
            for entry in app.wm_group_match_data[item_name]:
                app.drop_area.insert(tk.END, entry)
        else:
            app.drop_area.insert(tk.END, "No matching data found.")

        is_locked = app.lock_status.get(item_name, False)
        app.lock_button.config(text="Unlock" if is_locked else "Lock")
        app.drop_area.config(bg="gray" if is_locked else "white")
    else:
        app.center_title_label.config(text="")


def save_lock_status(app):
    try:
        with open("wm_group_match.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data["lock_status"] = app.lock_status

    with open("wm_group_match.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
