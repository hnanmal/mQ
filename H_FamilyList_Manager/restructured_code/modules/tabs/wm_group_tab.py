# modules/tabs/wm_group_tab.py

from tkinter import ttk, font
import tkinter as tk
from modules.data_manager import load_wm_group_match_data
from modules.utils.excel_utils import display_excel_data_openpyxl
from modules.drag_and_drop import DragAndDropManager

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

def create_wm_matching_by_group_tab(app):
    tab_frame = ttk.Frame(app.notebook)

    left_frame = tk.Frame(tab_frame, width=250)
    center_frame = tk.Frame(tab_frame, width=300)
    right_frame = tk.Frame(tab_frame)
    center_button_frame = tk.Frame(center_frame, width=50)

    tab_frame.grid_columnconfigure(0, weight=0)
    tab_frame.grid_columnconfigure(1, weight=0)
    tab_frame.grid_columnconfigure(2, weight=1)
    tab_frame.grid_rowconfigure(0, weight=1)

    left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    center_button_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    center_frame.grid_rowconfigure(0, weight=0)
    center_frame.grid_rowconfigure(1, weight=0)
    center_frame.grid_rowconfigure(2, weight=1)
    center_frame.grid_columnconfigure(0, weight=1)

    center_button_frame.grid_rowconfigure(0, weight=0)
    center_button_frame.grid_columnconfigure(0, weight=1)

    right_frame.grid_rowconfigure(0, weight=0)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    app.wm_group_treeview = ttk.Treeview(left_frame, columns=("name",), show="headings")
    app.wm_group_treeview.heading("name", text="Name")
    app.wm_group_treeview.column("name", width=240, anchor="w")
    app.wm_group_treeview.grid(row=0, column=0, sticky="nsew")

    fixed_title_label = ttk.Label(center_frame, text="          WM Matching          ", font=("Arial", 16, "bold"))
    fixed_title_label.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

    app.center_title_label = ttk.Label(center_frame, text="", font=("Arial", 14))
    app.center_title_label.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

    app.drop_area = tk.Listbox(center_frame, bg="white", relief="sunken", bd=2, selectmode=tk.SINGLE)
    app.drop_area.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    app.add_button = ttk.Button(center_button_frame, text="+", command=lambda: add_item_to_center(app))
    app.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="n")

    app.remove_button = ttk.Button(center_button_frame, text="-", command=lambda: remove_item_from_center(app))
    app.remove_button.grid(row=1, column=0, padx=5, pady=5, sticky="n")

    app.lock_button = ttk.Button(center_button_frame, text="Lock", command=lambda: toggle_lock(app, app.add_button, app.remove_button, app.lock_button))
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

    search_button = ttk.Button(search_frame, text="Search", command=lambda: filter_excel_data(app, search_var.get()))
    search_button.pack(side="left", padx=(5, 0))

    search_entry.bind("<Return>", lambda event: filter_excel_data(app, search_var.get()))

    excel_frame = tk.Frame(right_frame)
    excel_frame.grid(row=1, column=0, sticky="nsew")

    excel_frame.grid_rowconfigure(0, weight=1)
    excel_frame.grid_columnconfigure(0, weight=1)

    app.excel_treeview = ttk.Treeview(excel_frame, show="headings")
    app.excel_treeview.grid(row=0, column=0, sticky="nsew")

    scrollbar_x = ttk.Scrollbar(excel_frame, orient="horizontal", command=app.excel_treeview.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    app.excel_treeview.configure(xscrollcommand=scrollbar_x.set)

    scrollbar_y = ttk.Scrollbar(excel_frame, orient="vertical", command=app.excel_treeview.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    app.excel_treeview.configure(yscrollcommand=scrollbar_y.set)

    display_excel_data_openpyxl(app)

    app.notebook.add(tab_frame, text="WM 그룹별 매칭")

    app.wm_group_treeview.bind("<<TreeviewSelect>>", lambda event: update_center_title_label(app, event))

    app.wm_group_treeview.tag_configure("locked", background="gray")
    app.wm_group_treeview.tag_configure("unlocked", background="white")

    app.drag_and_drop_manager.enable_drag_and_drop()

    app.lock_status = {}

    load_wm_group_match_data(app)

    update_center_title_label(app, None)
