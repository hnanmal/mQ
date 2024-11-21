# src/views/widget/treeview_utils.py

import tkinter as tk
from tkinter import ttk


# Composition for Style Management
class DefaultTreeViewStyleManager:
    @staticmethod
    def apply_style(treeview):
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial", 10),
            highlightthickness=1,
            background="white",
            foreground="black",
            height=50,
        )
        style.map(
            "Treeview",
            background=[("selected", "#fffec0")],  # Set the selection background color
            foreground=[("selected", "blue")],
        )  # Set the selection foreground color
        style.configure("Treeview.Heading", font=("Arial", 10, "normal"))
        treeview.configure(style="Treeview")


# Composition for State Management
class TreeViewStateObserver:
    def __init__(self, state, treeview, updateFunc):
        self.state = state
        self.treeview = treeview
        # self.state.observer_manager.add_observer(self.update)
        self.state.observer_manager.add_observer(updateFunc)


class BaseTreeView:
    def __init__(self, parent, headers):
        self.tree = ttk.Treeview(parent, columns=headers, show="headings")
        self.setup_columns(headers)
        self.parent = parent

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

    def insert_data_with_levels(self, data, parent_id=""):
        """Insert data into the TreeView with levels based on nested dictionaries."""
        for classification, sub_dict in data.items():
            class_id = self.tree.insert(
                parent_id, "end", text=classification, values=(classification, "", "")
            )
            self.tree.item(class_id, open=True)

            for gwm, itemDicts in sub_dict.items():
                gwm_id = self.tree.insert(
                    class_id, "end", text=gwm, values=("", gwm, "")
                )
                self.tree.item(gwm_id, open=True)

                for item in itemDicts.keys():
                    self.tree.insert(gwm_id, "end", text=item, values=("", "", item))
                # for item in items:
                #     item_key = list(item.keys())[0]
                #     self.tree.insert(
                #         gwm_id, "end", text=item_key, values=("", "", item_key)
                #     )


class TeamStd_GWMTreeView:
    def __init__(self, state, parent):
        self.state = state
        headers = ["분류", "G-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        self.treeview = BaseTreeView(parent, headers)
        self.state_observer = TreeViewStateObserver(state, self.treeview, self.update)

        # Set up UI
        self.treeview.setup_columns(headers, hdr_widths)
        self.set_title(parent)
        self.treeview.tree.pack(expand=True, fill="both")

        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    # def update(self, state):
    def update(self, e):
        """Update the TreeView whenever the state changes."""
        if "std-GWM" in self.state.team_std_info:
            self.treeview.clear_treeview()
            data = self.state.team_std_info["std-GWM"]
            self.treeview.insert_data_with_levels(data)

    def set_title(self, parent):
        title_font = tk.font.Font(family="맑은 고딕", size=12)
        title_label = tk.Label(parent, text="Standard Types for GWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def on_item_selected(self, event):
        selected_item_id = self.treeview.tree.selection()

        # selected_item_id = self.treeview.tree.focus()
        # item_values = self.treeview.tree.item(selected_item, "values")

        # Collect all parent items to build the full path
        # current_item = selected_item
        parent_item_id = self.treeview.tree.parent(selected_item_id)
        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)
        selected_item_name = self.treeview.tree.item(selected_item_id, "values")[-1]

        parent_item_name = self.treeview.tree.item(parent_item_id, "values")[-2]
        grand_parent_item_name = self.treeview.tree.item(
            grand_parent_item_id, "values"
        )[-3]

        formatted_value = " | ".join(
            [
                grand_parent_item_name,
                parent_item_name,
                selected_item_name,
            ]
        )

        self.state.selected_stdGWM_item.set(formatted_value)
        # print(f"Selected Item: {self.state.selected_stdGWM_item.get()}")

        # ## 리스트뷰 업데이트 관련
        # if selected_item_id:
        #     # Fetch matched list items from state
        #     matching_list_items = self.state.team_std_info["std-GWM"][
        #         grand_parent_item_name
        #     ][parent_item_name][selected_item_name]
        #     print(matching_list_items)
        #     # Notify observers to update the list view
        #     # self.state.selected_tree_item = selected_item_id
        #     # self.state.update_stdGWM_matching(matching_list_items)


class TeamStd_GWMmatching_TreeView:
    def __init__(self, state, parent):
        self.state = state
        headers = ["Work Master"]
        hdr_widths = [500]

        # Compose TreeView, Style Manager, and State Observer
        self.treeview = BaseTreeView(parent, headers)
        # TreeViewStyleManager.apply_style(self.treeview.tree)
        self.state_observer = TreeViewStateObserver(state, self.treeview, self.update)

        # Set up UI
        self.treeview.setup_columns(headers, hdr_widths)
        self.set_title(parent)
        self.treeview.tree.pack(expand=True, fill="both")

        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    # def update(self, state):
    def update(self, e):
        """Update the TreeView whenever the state changes."""
        print("TeamStd_GWMmatching_TreeView > update 메소드 시작")
        print(self.state.selected_stdGWM_item.get())
        # try:
        #     self.state.selected_stdGWM_item.get().split(" | ")

        #     grand_parent_item_name, parent_item_name, selected_item_name = (
        #         self.state.selected_stdGWM_item.get().split(" | ")
        #     )
        #     if "std-GWM" in self.state.team_std_info:
        #         self.treeview.clear_treeview()
        #         data = self.state.team_std_info["std-GWM"][grand_parent_item_name][
        #             parent_item_name
        #         ][selected_item_name]
        #         self.treeview.insert_data(data)
        # except:
        #     print("TeamStd_GWMmatching_TreeView > update 메소드 진입 안됩니다~")
        #     pass

    def set_title(self, parent):
        title_font = tk.font.Font(family="맑은 고딕", size=12)
        title_label = tk.Label(parent, text="Standard Types for GWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def on_item_selected(self, event):
        pass
