# modules/tabs/wm_group_tab.py

from tkinter import ttk, font
import tkinter as tk
from modules.data_manager import load_wm_group_match_data
from modules.utils.excel_utils import display_excel_data_openpyxl
from modules.drag_and_drop import DragAndDropManager
import json


def get_item_texts(item_values):
    res = [
        item_values[0],
        item_values[3],
        item_values[5],
        item_values[7],
        item_values[9],
        item_values[11],
        item_values[13],
        item_values[15],
        item_values[17],
        item_values[19],
        item_values[21],
        item_values[23],
    ]
    return res


def add_item_to_center(app):
    selected_items = app.excel_treeview.selection()
    if not selected_items:
        tk.messagebox.showwarning(
            "No Selection", "Please select an item from the Excel data."
        )
        return

    for item in selected_items:
        item_values = app.excel_treeview.item(item, "values")
        # Get the 0th, 7th, and 9th column values
        item_texts = get_item_texts(item_values)
        item_string = " - ".join(item_texts)

        # Insert all selected values into the Listbox
        app.drop_area.insert(
            tk.END,
            item_string,
        )  # Insert item text into the Listbox


def save_to_json(data, filename="wm_group_match.json"):
    """Saves the given dictionary to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def remove_item_from_center(app):
    selected_index = app.drop_area.curselection()
    if selected_index:
        app.drop_area.delete(selected_index)


class WM_group_tab_Manager:
    def __init__(self, app):
        self.app = app

    def update_wm_group_matching_treeview(self, level_6_items):
        # Clear the current content of the Treeview
        self.app.wm_group_treeview.delete(*self.app.wm_group_treeview.get_children())

        # Insert the unique names into the Treeview
        for name in level_6_items:
            self.app.wm_group_treeview.insert("", tk.END, values=(name,))

    def update_center_title_label(self, event):
        # Reload the WM Group Match data from the JSON file
        self.wm_group_match_data = self.load_wm_group_match_data()

        # Get the selected item
        selected_item = self.app.wm_group_treeview.selection()

        if selected_item:
            # Get the value of the selected item (the name)
            item_name = self.app.wm_group_treeview.item(selected_item[0], "values")[0]

            # Update the center title label with the selected item's name
            self.app.center_title_label.config(text=item_name)

            # Clear the current content in the center area
            self.app.drop_area.delete(0, tk.END)

            # Check if there is matching data in wm_group_match.json
            if item_name in self.wm_group_match_data:
                # Populate the center area with the matched data
                for entry in self.wm_group_match_data[item_name]:
                    self.app.drop_area.insert(tk.END, entry)
            else:
                # If no match is found, leave the area empty
                self.app.drop_area.insert(tk.END, "No matching data found.")

            # Update the lock button state and center area background color
            is_locked = self.app.lock_status.get(item_name, False)
            self.app.lock_button.config(text="Unlock" if is_locked else "Lock")
            self.app.drop_area.config(bg="gray" if is_locked else "white")

        else:
            # Clear the label if no item is selected
            self.app.center_title_label.config(text="")

    def create_wm_matching_by_group_tab(app):
        # Create a frame for the new tab using tk.Frame
        tab_frame = ttk.Frame(app.notebook)

        # Split the frame into left, center, and right areas using tk.Frame
        left_frame = tk.Frame(tab_frame, width=250)
        center_frame = tk.Frame(tab_frame, width=300)
        right_frame = tk.Frame(tab_frame)
        center_button_frame = tk.Frame(center_frame, width=50)  # Frame for the buttons

        # Configure grid layout for the tab_frame
        tab_frame.grid_columnconfigure(0, weight=0)
        tab_frame.grid_columnconfigure(1, weight=0)
        tab_frame.grid_columnconfigure(2, weight=1)
        tab_frame.grid_rowconfigure(0, weight=1)

        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        center_button_frame.grid(
            row=2, column=1, sticky="nsew", padx=5, pady=5
        )  # Place the button frame
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        center_frame.grid_rowconfigure(0, weight=0)
        center_frame.grid_rowconfigure(1, weight=0)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)

        center_button_frame.grid_rowconfigure(
            0, weight=0
        )  # Align with the top of the area
        center_button_frame.grid_columnconfigure(0, weight=1)

        right_frame.grid_rowconfigure(0, weight=0)  # Adjusted to make space for search
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Create a Treeview to display the unique names without indents in the left area
        app.wm_group_treeview = ttk.Treeview(
            left_frame, columns=("name",), show="headings"
        )
        app.wm_group_treeview.heading("name", text="Name")
        app.wm_group_treeview.column("name", width=240, anchor="w")
        app.wm_group_treeview.grid(row=0, column=0, sticky="nsew")

        # Add a vertical scrollbar to the left area
        left_scrollbar = ttk.Scrollbar(
            left_frame, orient="vertical", command=app.wm_group_treeview.yview
        )
        app.wm_group_treeview.configure(yscrollcommand=left_scrollbar.set)
        left_scrollbar.grid(row=0, column=1, sticky="ns")

        # Add horizontal and vertical scrollbars to the center area
        center_scrollbar_x = ttk.Scrollbar(
            center_frame, orient="horizontal", command=app.drop_area.xview
        )
        app.drop_area.configure(xscrollcommand=center_scrollbar_x.set)
        center_scrollbar_x.grid(row=3, column=0, sticky="ew")

        # Create a fixed title label in the center area
        fixed_title_label = ttk.Label(
            center_frame,
            text="          WM Matching          ",
            font=("Arial", 16, "bold"),
        )
        fixed_title_label.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

        # Create a dynamic title label in the center area
        app.center_title_label = ttk.Label(center_frame, text="", font=("Arial", 14))
        app.center_title_label.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

        # Create a Listbox for the drop area to hold multiple items and allow selection
        app.drop_area = tk.Listbox(
            center_frame, bg="white", relief="sunken", bd=2, selectmode=tk.SINGLE
        )
        app.drop_area.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Add + and - buttons to the center_button_frame
        app.add_button = ttk.Button(
            center_button_frame, text="+", command=lambda: add_item_to_center(app)
        )
        app.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        app.remove_button = ttk.Button(
            center_button_frame, text="-", command=lambda: remove_item_from_center(app)
        )
        app.remove_button.grid(row=1, column=0, padx=5, pady=5, sticky="n")

        app.lock_button = ttk.Button(
            center_button_frame,
            text="Lock",
            command=lambda: toggle_lock(
                app, app.add_button, app.remove_button, app.lock_button
            ),
        )
        app.lock_button.grid(row=2, column=0, padx=5, pady=5, sticky="n")

        search_frame = tk.Frame(right_frame)
        search_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Setup the search box and button
        app.search_manager.setup_search(search_frame)

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side="left", padx=(0, 5))

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side="left", fill="x", expand=True)

        search_button = ttk.Button(
            search_frame,
            text="Search",
            command=lambda: filter_excel_data(app, search_var.get()),
        )
        search_button.pack(side="left", padx=(5, 0))

        search_entry.bind(
            "<Return>", lambda event: filter_excel_data(app, search_var.get())
        )

        excel_frame = tk.Frame(right_frame)
        excel_frame.grid(row=1, column=0, sticky="nsew")

        excel_frame.grid_rowconfigure(0, weight=1)
        excel_frame.grid_columnconfigure(0, weight=1)

        app.excel_treeview = ttk.Treeview(excel_frame, show="headings")
        app.excel_treeview.grid(row=0, column=0, sticky="nsew")

        scrollbar_x = ttk.Scrollbar(
            excel_frame, orient="horizontal", command=app.excel_treeview.xview
        )
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        app.excel_treeview.configure(xscrollcommand=scrollbar_x.set)

        scrollbar_y = ttk.Scrollbar(
            excel_frame, orient="vertical", command=app.excel_treeview.yview
        )
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        app.excel_treeview.configure(yscrollcommand=scrollbar_y.set)

        display_excel_data_openpyxl(app)

        app.notebook.add(tab_frame, text="WM 그룹별 매칭")

        app.wm_group_treeview.bind(
            "<<TreeviewSelect>>", lambda event: update_center_title_label(app, event)
        )

        app.wm_group_treeview.tag_configure("locked", background="gray")
        app.wm_group_treeview.tag_configure("unlocked", background="white")

        app.drag_and_drop_manager.enable_drag_and_drop()

        app.lock_status = {}

        load_wm_group_match_data(app)

        update_center_title_label(app, None)
