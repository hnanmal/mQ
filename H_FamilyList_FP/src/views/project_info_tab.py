import tkinter as tk
from tkinter import ttk

def create_project_info_tab(notebook, state):
    """Create the '프로젝트 정보 입력' tab with two sections."""
    project_info_tab = ttk.Frame(notebook)
    notebook.add(project_info_tab, text="프로젝트 정보 입력")

    # Divide the tab into two sections (frames)
    section1 = ttk.Frame(project_info_tab, width=300, height=200)
    section2 = ttk.Frame(project_info_tab, width=400, height=200)

    section1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    section2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    section1.pack_propagate(False)
    section2.pack_propagate(False)

    # Section 1 - Project Name Input
    project_name_label = ttk.Label(section1, text="Project Name", font=("Arial", 14))
    project_name_label.pack(pady=10, anchor="w")

    # Project Name Entry field
    project_name_var = tk.StringVar()
    project_name_entry = ttk.Entry(section1, textvariable=project_name_var, width=30)
    project_name_entry.pack(pady=10, anchor="w")

    # Save Project Name button
    def save_project_name():
        state["project_name"] = project_name_var.get()
        print(f"Project Name saved: {state['project_name']}")

    save_project_button = ttk.Button(section1, text="Save Project Name", command=save_project_name)
    save_project_button.pack(pady=10, anchor="w")

    # Building List Title
    building_list_label = ttk.Label(section1, text="Building List", font=("Arial", 14))
    building_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar with reduced width
    listbox_frame = ttk.Frame(section1, width=300)
    listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Function to auto-number the buildings
    def auto_numbering():
        items = building_treeview.get_children()
        if not items:
            return  # Do nothing if there are no items

        start_number = 1
        first_item_values = building_treeview.item(items[0], "values")
        if first_item_values[1]:  # If the first item has a number, start from it
            try:
                start_number = int(first_item_values[1])
            except ValueError:
                pass  # If it's not a valid number, start from 1

        for idx, item in enumerate(items):
            building_treeview.set(item, "Number", start_number + idx)

    # Auto Numbering Button (moved to top right corner of listbox_frame)
    auto_number_button = ttk.Button(listbox_frame, text="Auto Numbering", command=auto_numbering)
    auto_number_button.pack(side=tk.TOP, padx=5, pady=5, anchor="e")

    # Create Treeview widget with two columns: one for Building Name and one for Number
    building_treeview = ttk.Treeview(listbox_frame, columns=("Building Name", "Number"), show="headings", height=8)
    building_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define the headings
    building_treeview.heading("Building Name", text="Building Name")
    building_treeview.heading("Number", text="Number")

    # Define column width
    building_treeview.column("Building Name", width=150)
    building_treeview.column("Number", width=100)

    # Add vertical scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=building_treeview.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    building_treeview.config(yscrollcommand=scrollbar.set)

    # Multi-line Text widget for adding new buildings
    new_building_text = tk.Text(section1, height=4, width=30)
    new_building_text.pack(pady=5, anchor="w")

    # Function to add new buildings to the Treeview
    def add_building():
        building_input = new_building_text.get("1.0", tk.END).strip()
        if building_input:
            # Split the input by newlines and add each line as a separate item
            buildings = building_input.split("\n")
            for building in buildings:
                if building.strip():  # Avoid adding empty lines
                    building_treeview.insert("", "end", values=(building.strip(), ""))
            new_building_text.delete("1.0", tk.END)  # Clear the input field

    # Function to remove the selected building(s) from the Treeview
    def remove_building():
        selected_items = building_treeview.selection()
        for item in selected_items:
            building_treeview.delete(item)

    # Add and Remove buttons
    add_button = ttk.Button(section1, text="Add", command=add_building)
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    remove_button = ttk.Button(section1, text="Remove", command=remove_building)
    remove_button.pack(side=tk.LEFT, padx=5, pady=5)



    # Enable in-place editing of the "Number" column on single click
    def on_click_edit(event):
        selected_item = building_treeview.selection()[0]
        column = building_treeview.identify_column(event.x)
        row = building_treeview.identify_row(event.y)
        
        if column == "#2":  # If the "Number" column is clicked
            # Create an Entry widget directly in the Treeview cell
            x, y, width, height = building_treeview.bbox(selected_item, "Number")
            entry = ttk.Entry(building_treeview)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, building_treeview.item(selected_item, "values")[1])

            # Function to save the edited value
            def save_edit(event=None):
                building_treeview.set(selected_item, column="Number", value=entry.get())
                entry.destroy()  # Remove the Entry widget

            entry.bind("<Return>", save_edit)  # Save on pressing Enter
            entry.bind("<FocusOut>", save_edit)  # Save on focus out

            entry.focus()  # Set focus to the Entry widget

    building_treeview.bind("<Button-1>", on_click_edit)  # Bind single click to edit

    # Save button to store the building list into the state
    def save_building_list():
        building_list = [
            building_treeview.item(item, "values")
            for item in building_treeview.get_children()
        ]
        state["building_list"] = building_list
        print(f"Building List saved: {state['building_list']}")

    save_building_button = ttk.Button(section1, text="Save Building List", command=save_building_list)
    save_building_button.pack(pady=10, anchor="w")

    return project_info_tab
