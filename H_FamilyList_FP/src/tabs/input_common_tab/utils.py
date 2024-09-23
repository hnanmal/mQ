# src/tabs/input_common_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from src.tabs.project_info_tab.common_utils import on_click_edit


def create_defaultTreeview(state, frame, columns, height=None):
    # Define the columns for the Treeview
    # columns = ("Name", "Age", "City")

    # Create the Treeview with columns
    tree = (
        ttk.Treeview(frame, columns=columns, show="headings", height=height)
        if height
        else ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
        )
    )

    # # Define the column headings
    for col in columns:
        tree.heading(col, text=col)

    # # Define the column properties (width, alignment)
    for col in columns:
        tree.column(col, width=70, anchor="center")

    # Add a scrollbar (optional)
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    # Pack the Treeview into the window
    tree.pack(fill=tk.BOTH, expand=True)

    tree.bind("<Double-Button-1>", lambda e: on_click_edit(e, state, tree))

    return tree


def add_common_param(state, treeview, new_param_text):
    param_input = new_param_text.get("1.0", tk.END).strip()
    if param_input:
        params = param_input.split("\n")
        for param in params:
            if param.strip():
                param_name, param_input, param_unit, param_disc = param.split(",")
                treeview.insert(
                    "",
                    "end",
                    values=(param_name, param_input, param_unit, param_disc),
                )
                state.logging_text_widget.write(f"add [ {param_name} ] item.\n")
        new_param_text.delete("1.0", tk.END)


def save_project_common_info(state, earth_treeview, steel_treeview):
    # Save project_info in the state

    # Function to retrieve all headers
    def get_treeview_headers(tree):
        headers = []
        for col in tree["columns"]:
            header = tree.heading(col)["text"]
            headers.append(header)
        return headers

    earth_headers = get_treeview_headers(earth_treeview)
    earth_commons = []
    for item in earth_treeview.get_children():
        tmp_earth = {}
        for k, v in zip(earth_headers, earth_treeview.item(item).get("values")):
            tmp_earth[k] = v
        earth_commons.append(tmp_earth)

    steel_headers = get_treeview_headers(steel_treeview)
    steel_commons = []
    for item in steel_treeview.get_children():
        tmp_steel = {}
        for k, v in zip(steel_headers, steel_treeview.item(item).get("values")):
            tmp_steel[k] = v
        steel_commons.append(tmp_steel)

    state.project_info["common_info"]["earth"] = earth_commons
    state.project_info["common_info"]["steel"] = steel_commons
    project_info_ = state.project_info
    # earth_treeview.get_children()

    # Save to file
    # file_path = f"{project_info_['project_name']}_pjt_info.json"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Default file extension
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")
