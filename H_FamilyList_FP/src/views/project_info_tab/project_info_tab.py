import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json


def create_project_info_tab(notebook, state):
    """Create the '프로젝트 정보 입력' tab with two sections."""
    project_info_tab = ttk.Frame(notebook)
    notebook.add(project_info_tab, text="프로젝트 정보 입력")

    # Divide the tab into three sections (frames)
    section1 = ttk.Frame(project_info_tab, width=300, height=200)
    section2 = ttk.Frame(project_info_tab, width=400, height=200)
    section3 = ttk.Frame(project_info_tab, width=400, height=200)

    section1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    section2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    section3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    section1.pack_propagate(False)
    section2.pack_propagate(False)
    section3.pack_propagate(False)

    # Load Project Info Button
    def load_project_info():
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)

            # Save loaded data to state
            state["project_info"] = loaded_data

            # Populate UI fields from project_info
            project_name_var.set(loaded_data.get("project_name", ""))
            project_type_var.set(loaded_data.get("project_type", ""))

            # Clear and populate the building treeview
            building_treeview.delete(*building_treeview.get_children())
            for building_name, building_data in loaded_data.get(
                "building_list", {}
            ).items():
                building_treeview.insert(
                    "",
                    "end",
                    values=(
                        building_data["building_name"],
                        building_data["building_number"],
                    ),
                )

            # Clear and populate finish types for the selected building
            finish_listbox.delete(0, tk.END)
            selected_building = building_treeview.selection()
            if selected_building:
                selected_building_name = building_treeview.item(
                    selected_building[0], "values"
                )[0]
                finish_types = (
                    loaded_data.get("building_list", {})
                    .get(selected_building_name, {})
                    .get("finish_types", [])
                )
                for finish_type in finish_types:
                    finish_listbox.insert(tk.END, finish_type)

            print(f"Project Info loaded from {file_path}")

    def save_project_info():
        # Check if the state contains a 'finish_types' attribute, or create one
        finish_types_data = getattr(state, "finish_types", {})

        # Consolidate all relevant data into the project_info dictionary
        project_info = {
            "project_name": project_name_var.get(),
            "project_type": project_type_var.get(),
            "building_list": {
                building_treeview.item(item, "values")[0]: {
                    "building_name": building_treeview.item(item, "values")[0],
                    "building_number": building_treeview.item(item, "values")[1]
                    or None,
                    "finish_types": finish_types_data.get(
                        building_treeview.item(item, "values")[0], []
                    ),
                }
                for item in building_treeview.get_children()
            },
        }

        # Save project_info in the state
        state.project_info = project_info

        # Save to file
        file_path = f"{project_info['project_name']}_pjt_info.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(project_info, f, ensure_ascii=False, indent=4)
        print(f"Project Info saved to {file_path}")

    load_info_button = ttk.Button(
        section1, text="Load Project Info", command=load_project_info
    )
    load_info_button.pack(pady=10, anchor="w")

    save_info_button = ttk.Button(
        section1, text="Save Project Info", command=save_project_info
    )
    save_info_button.pack(pady=10, anchor="w")

    # Section 1 - Project Info
    project_name_label = ttk.Label(section1, text="Project Name", font=("Arial", 14))
    project_name_label.pack(pady=10, anchor="w")

    project_name_var = tk.StringVar()
    project_name_entry = ttk.Entry(section1, textvariable=project_name_var, width=30)
    project_name_entry.pack(pady=10, anchor="w")

    # Project Type Label and Dropdown
    project_type_label = ttk.Label(section1, text="Project Type", font=("Arial", 14))
    project_type_label.pack(pady=10, anchor="w")

    project_type_var = tk.StringVar()
    project_type_dropdown = ttk.Combobox(
        section1, textvariable=project_type_var, values=["Execution", "Bid"]
    )
    project_type_dropdown.pack(pady=10, anchor="w")

    # Building List Title
    building_list_label = ttk.Label(section1, text="Building List", font=("Arial", 14))
    building_list_label.pack(pady=10, anchor="w")

    # Frame for Treeview and Scrollbar
    listbox_frame = ttk.Frame(section1, width=300)
    listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

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
            building_name = building_treeview.item(item, "values")[0]
            building_treeview.set(item, "Number", start_number + idx)

            # Update the building list in the state with new numbers
            if building_name in state["building_list"]:
                state["building_list"][building_name]["building_number"] = (
                    start_number + idx
                )

    auto_number_button = ttk.Button(
        listbox_frame, text="Auto Numbering", command=auto_numbering
    )
    auto_number_button.pack(side=tk.TOP, padx=5, pady=5, anchor="e")

    building_treeview = ttk.Treeview(
        listbox_frame, columns=("Building Name", "Number"), show="headings", height=8
    )
    building_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    building_treeview.heading("Building Name", text="Building Name")
    building_treeview.heading("Number", text="Number")

    building_treeview.column("Building Name", width=150)
    building_treeview.column("Number", width=100)

    scrollbar = ttk.Scrollbar(
        listbox_frame, orient=tk.VERTICAL, command=building_treeview.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    building_treeview.config(yscrollcommand=scrollbar.set)

    new_building_text = tk.Text(section1, height=4, width=30)
    new_building_text.pack(pady=5, anchor="w")

    def add_building():
        building_input = new_building_text.get("1.0", tk.END).strip()
        if building_input:
            buildings = building_input.split("\n")
            for building in buildings:
                if building.strip():
                    building_treeview.insert("", "end", values=(building.strip(), ""))
            new_building_text.delete("1.0", tk.END)

    def remove_building():
        selected_items = building_treeview.selection()
        for item in selected_items:
            building_treeview.delete(item)

    add_button = ttk.Button(section1, text="Add", command=add_building)
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    remove_button = ttk.Button(section1, text="Remove", command=remove_building)
    remove_button.pack(side=tk.LEFT, padx=5, pady=5)

    def on_click_edit(event):
        if building_treeview.selection():
            selected_item = building_treeview.selection()[0]
            column = building_treeview.identify_column(event.x)
            if column == "#2":
                x, y, width, height = building_treeview.bbox(selected_item, "Number")
                entry = ttk.Entry(building_treeview)
                entry.place(x=x, y=y, width=width, height=height)
                entry.insert(0, building_treeview.item(selected_item, "values")[1])

                def save_edit(event=None):
                    building_treeview.set(
                        selected_item, column="Number", value=entry.get()
                    )
                    entry.destroy()

                entry.bind("<Return>", save_edit)
                entry.bind("<FocusOut>", save_edit)
                entry.focus()

    building_treeview.bind("<Button-1>", on_click_edit)

    # Section 2 - Selected Building and Finish Type
    selected_building_label = ttk.Label(
        section2, text="Selected Building: ", font=("Arial", 14)
    )
    selected_building_label.pack(pady=10, anchor="w")

    # Add Treeview Selection Binding
    def on_building_select(event):
        selected_item = building_treeview.selection()
        if selected_item:
            selected_building = building_treeview.item(selected_item[0])["values"][0]
            selected_building_label.config(
                text=f"Selected Building: {selected_building}"
            )

    building_treeview.bind("<<TreeviewSelect>>", on_building_select)

    finish_type_list_label = ttk.Label(
        section2, text="Finish Type List", font=("Arial", 14)
    )
    finish_type_list_label.pack(pady=10, anchor="w")

    finish_listbox = tk.Listbox(section2, height=8)
    finish_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Add Finish Type functionality
    def add_finish_type():
        finish_type = new_finish_text.get("1.0", tk.END).strip()
        if finish_type:
            selected_item = building_treeview.selection()
            if selected_item:
                building_name = building_treeview.item(selected_item[0], "values")[0]
                finish_listbox.insert(tk.END, finish_type)

                # Update state for the selected building
                if "finish_types" not in state:
                    state["finish_types"] = {}
                if building_name not in state["finish_types"]:
                    state["finish_types"][building_name] = []
                state["finish_types"][building_name].append(finish_type)

                new_finish_text.delete("1.0", tk.END)

    def remove_finish_type():
        selected_items = finish_listbox.curselection()
        for item in reversed(selected_items):
            finish_listbox.delete(item)

    new_finish_text = tk.Text(section2, height=2, width=30)
    new_finish_text.pack(pady=5)

    add_type_button = ttk.Button(section2, text="Add Type", command=add_finish_type)
    add_type_button.pack(side=tk.LEFT, padx=5, pady=5)

    remove_type_button = ttk.Button(
        section2, text="Remove Type", command=remove_finish_type
    )
    remove_type_button.pack(side=tk.LEFT, padx=5, pady=5)

    return project_info_tab
