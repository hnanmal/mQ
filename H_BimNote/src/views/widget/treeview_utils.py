# src/views/widget/treeview_utils.py

import tkinter as tk
from tkinter import ttk


def get_tree_item_value(tree, _item):
    item_values = tree.item(_item, "values")
    return item_values


class BaseTreeView:
    def __init__(self, parent, headers):
        self.tree = ttk.Treeview(parent, columns=headers, show="headings")
        self.setup_columns(headers)
        self.parent = parent
        # self.tree.pack(expand=True, fill="both")

    def setup_columns(self, headers, hdr_widths=None):
        for idx, header in enumerate(headers):
            self.tree.heading(header, text=header)
            if hdr_widths:
                self.tree.column(header, width=hdr_widths[idx])

    def insert_data(self, data):
        for row in data:
            self.tree.insert("", "end", values=row)

    def clear_treeview(self):
        """Clear all items from the Treeview."""
        self.tree.delete(*self.tree.get_children())

    def get_tree_data(self):
        """Get the current data from the Treeview as a list of dictionaries."""
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            data.append(dict(zip(self.tree["columns"], values)))
        return data


class ProjectTreeView(BaseTreeView):
    def __init__(self, parent):
        headers = ["Project Name", "Description", "Start Date", "End Date"]
        super().__init__(parent, headers)

    def load_project_data(self, project_data):
        """Load data specific to projects."""
        self.insert_data(project_data)


class TeamStd_GWMTreeView(BaseTreeView):
    def __init__(self, state, parent):
        self.state = state
        headers = ["분류", "G-WM", "Item"]
        super().__init__(parent, headers)
        hdr_widths = [127, 60, 100]
        self.setup_columns(headers, hdr_widths)

        self.set_title_and_packing()
        # Add itself as an observer to the state
        self.state.observer_manager.add_observer(self.update)

        # Bind the selection event
        self.tree.bind("<<TreeviewSelect>>", lambda e: self.on_select(e))
        self.tree.bind("<KeyRelease>", lambda e: self.on_key_release(e))

    def set_title_and_packing(self):
        self.set_treeview_style()

        title_font = tk.font.Font(
            family="맑은 고딕",
            size=12,
            # weight="bold",
        )
        title_label = tk.Label(
            self.parent,
            text="Group Work Master",
            font=title_font,
        )
        title_label.pack(padx=5, pady=5, anchor="w")
        self.tree.pack(expand=True, fill="both")

    def set_treeview_style(self):
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10))
        style.configure(
            "Treeview.Heading", font=("Arial", 10, "normal")
        )  # 헤더 폰트 스타일 조정

    def insert_data_with_levels(self, data, parent_id=""):
        """Insert data into the TreeView with levels based on nested dictionaries."""
        for classification, sub_dict in data.items():
            # Insert the classification level
            class_id = self.tree.insert(
                parent_id, "end", text=classification, values=(classification, "", "")
            )
            self.tree.item(class_id, open=True)  # Automatically expand this level
            self.unselectable_items.add(class_id)

            for gwm, items in sub_dict.items():
                # Insert the G-WM level
                gwm_id = self.tree.insert(
                    class_id, "end", text=gwm, values=("", gwm, "")
                )
                self.tree.item(gwm_id, open=True)  # Automatically expand this level
                self.unselectable_items.add(gwm_id)

                for item in items:
                    # Insert the Item level
                    item_key = list(item.keys())[0]  # Extract key from dict
                    item_id = self.tree.insert(
                        gwm_id, "end", text=item_key, values=("", "", item_key)
                    )
                    self.tree.item(
                        item_id, open=True
                    )  # Automatically expand this level

    def load_DB_data(self, db_data):
        """Load data specific to teams."""
        formatted_data = self.format_DB_data_for_treeview(db_data)
        # formatted_data = team_data
        self.insert_data(formatted_data)

    def format_DB_data_for_treeview(self, db_data):
        """Format the team data into a list suitable for inserting into the treeview."""
        formatted_data = []
        for classification, sub_dict in db_data.items():
            # formatted_data.append([classification, "", ""])
            formatted_data.append(["", "", ""])
            for gwm, items in sub_dict.items():
                # formatted_data.append(["", gwm, ""])
                formatted_data.append(["", "", ""])
                for item in items:
                    item_key = list(item.keys())[0]  # Extract key from dict
                    formatted_data.append([classification, gwm, item_key])
        return formatted_data

    def update(self, state):
        """Update the TreeView whenever the state changes."""
        if "std-GWM" in state.team_std_info:
            # Clear the existing TreeView and reload data from the updated state
            self.clear_treeview()
            # self.load_DB_data(state.team_std_info["std-GWM"])
            self.insert_data_with_levels(state.team_std_info["std-GWM"])

    def on_select(self, event):
        self.on_item_selected(event)

    def on_key_release(self, event):
        # This event is triggered when an arrow key is released
        if event.keysym in ["Up", "Down"]:
            self.on_item_selected()

    def on_item_selected(self, event):
        """Handle item selection and update the selected item's value in the state."""
        selected_item = self.tree.focus()

        item_values = self.tree.item(selected_item, "values")

        # Collect all parent items to build the full path
        # item_hierarchy = []
        current_item = selected_item
        parent_item = self.tree.parent(current_item)
        grand_parent_item = self.tree.parent(parent_item)

        formatted_value = " | ".join(
            [
                self.tree.item(grand_parent_item, "values")[-3],
                self.tree.item(parent_item, "values")[-2],
                item_values[-1],
            ]
        )

        self.state.selected_stdGWM_item.set(formatted_value)
        print(f"Selected Item: {self.state.selected_stdGWM_item.get()}")
