# src/views/wm_group_matching.py

import tkinter as tk
from tkinter import ttk

from src.controllers.logic import lock_toggle_logic
from src.views.excel_view import load_and_display_excel_with_search
from src.views.listbox_utils import (
    add_selected_row_to_listbox,
    display_level_6_items_list,
    remove_selected_items_from_listbox,
    update_level_6_items_list,
)


def update_listbox_item_styles(state, listbox, wm_group_manager):
    """Update the left listbox item styles based on lock status."""
    wm_group_data = wm_group_manager.get_wm_group_data()
    state.wm_group_data = wm_group_data
    # print(state.wm_group_data)

    for index in range(listbox.size()):
        item_name = listbox.get(index)

        # Check lock status for each item and apply background color
        if item_name in wm_group_data and wm_group_data[item_name].get("locked", False):
            listbox.itemconfig(index, {"bg": "#e2e2e2"})  # Light gray for locked items
        else:
            listbox.itemconfig(
                index, {"bg": "white"}
            )  # Default white for unlocked items


def create_wm_group_matching_tab(notebook, state, wm_group_manager):
    logging_text_widget = state.logging_text_widget
    # Log the start of loading
    logging_text_widget.write("Configuring system...\n")

    # Define the function to handle item selection
    def on_select_item(item_name):
        section2_label.config(text=item_name)

        # Clear the center listbox when a new item is selected
        center_listbox.config(state="normal")  # Temporarily enable to clear items
        center_listbox.delete(0, tk.END)

        # Retrieve the matching data from wm_group_manager
        wm_group_data = wm_group_manager.get_wm_group_data()

        # Check if the selected item has matching data in the wm_group_data
        if item_name in wm_group_data:
            # center_listbox.delete(0, tk.END)
            matched_data = wm_group_data[item_name].get("matched_items", [])
            locked_status = wm_group_data[item_name].get("locked", False)

            # Insert the matched data into the center listbox
            for item in matched_data:
                center_listbox.insert(tk.END, item)

            # If the item is locked, apply the locked style
            if locked_status:
                center_listbox.config(state="disabled", bg="#e2e2e2")
                add_button.config(state="disabled")
                del_button.config(state="disabled")
                lock_button.config(
                    text="Unlock"
                )  # Set button text to 'Unlock' when locked
            else:
                center_listbox.config(state="normal", bg="white")
                add_button.config(state="normal")
                del_button.config(state="normal")
                lock_button.config(
                    text="Lock"
                )  # Set button text to 'Lock' when unlocked
        else:
            # No matched data found for the selected item, enable the center_listbox and buttons
            center_listbox.config(state="normal", bg="white")
            add_button.config(state="normal")
            del_button.config(state="normal")
            lock_button.config(text="Lock")  # Set button text to 'Lock' when unlocked

        # Clear focus and selection after action to ensure no interference
        update_listbox_item_styles(state, left_listbox, wm_group_manager)
        # center_listbox.selection_clear(0, tk.END)

    """Create the WM Group Matching tab divided into three sections."""
    wm_group_matching_tab = ttk.Frame(notebook)
    notebook.add(wm_group_matching_tab, text="WM Group Matching")

    main_paned_window = tk.PanedWindow(
        wm_group_matching_tab,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    main_paned_window.pack(padx=10, pady=10, anchor="w", fill=tk.BOTH, expand=True)

    # Create three frames for the sections
    section1 = ttk.Frame(wm_group_matching_tab, width=300, height=200)
    section2 = ttk.Frame(wm_group_matching_tab, width=400, height=200)  # Fixed size
    section3 = ttk.Frame(wm_group_matching_tab)

    section1.pack(side=tk.LEFT, fill=tk.BOTH)
    section2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    section3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    main_paned_window.add(section1, stretch="always")
    main_paned_window.add(section2, stretch="always")
    main_paned_window.add(section3, stretch="always")

    # section2.pack_propagate(False)  # Prevent section2 from resizing

    # Create a label in Section 2 to display the selected item's name
    section2_label = ttk.Label(
        section2, text="Please Select Item", font=("Arial", 14), justify="left"
    )
    section2_label.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nw")

    # Create a frame to hold the Listbox and scrollbars
    center_listbox_frame = ttk.Frame(section2)
    center_listbox_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Make sure the listbox frame expands properly
    section2.grid_rowconfigure(2, weight=1)
    section2.grid_columnconfigure(0, weight=1)

    # Create scrollbars
    vertical_scrollbar = ttk.Scrollbar(center_listbox_frame, orient=tk.VERTICAL)
    horizontal_scrollbar = ttk.Scrollbar(center_listbox_frame, orient=tk.HORIZONTAL)

    # Create the listbox in the center area for matched items
    center_listbox = tk.Listbox(
        center_listbox_frame,
        selectmode=tk.EXTENDED,
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
        height=15,
        font=("Arial", 10),
        activestyle="dotbox",
    )

    # Use grid layout for precise control
    center_listbox.grid(row=0, column=0, sticky="nsew")

    # Configure scrollbars
    vertical_scrollbar.config(command=center_listbox.yview)
    horizontal_scrollbar.config(command=center_listbox.xview)

    # Grid the scrollbars
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    # Make sure the listbox and scrollbars resize properly
    center_listbox_frame.grid_rowconfigure(0, weight=1)
    center_listbox_frame.grid_columnconfigure(0, weight=1)

    # Create a frame for the buttons and place them vertically
    button_frame = ttk.Frame(section2)
    button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ns")

    # Add button to move selected Excel row to center listbox
    add_button = ttk.Button(
        button_frame,
        text="Add",
        command=lambda: add_selected_row_to_listbox(sheet_widget, center_listbox),
    )
    add_button.pack(side=tk.TOP, pady=5)

    # Del button to remove selected items from center listbox
    del_button = ttk.Button(
        button_frame,
        text="Del",
        command=lambda: remove_selected_items_from_listbox(center_listbox),
    )
    del_button.pack(side=tk.TOP, pady=5)

    # Lock button to lock the listbox and disable add/del buttons
    lock_button = ttk.Button(
        section2,
        text="Lock",
        command=lambda: lock_toggle_logic(
            state,
            wm_group_manager,
            section2_label["text"],
            center_listbox,
            add_button,
            del_button,
            lock_button,
        ),
    )
    lock_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    left_list_update_btn = ttk.Button(
        section1,
        text="refresh",
        command=lambda: update_level_6_items_list(
            state, section1, left_listbox, on_select_item
        ),
    )
    left_list_update_btn.pack()

    # Display the level 6 items in Section 1 as a Listbox and get the listbox instance
    left_listbox = display_level_6_items_list(state, section1, on_select_item)

    # After initializing all components, move to Excel loading
    def after_excel_load():
        """Call this after Excel data is loaded and highlighted."""
        logging_text_widget.write(
            "Loading complete.\n패밀리리스트에 오신것을 환영합니다..\n"
        )

    # In the third section, read and display the Excel file using tksheet
    sheet_widget = load_and_display_excel_with_search(
        section3,
        wm_group_manager,
        logging_text_widget,
        after_excel_load,
    )

    # Initialize the left listbox with the styles reflecting lock status
    update_listbox_item_styles(state, left_listbox, wm_group_manager)
