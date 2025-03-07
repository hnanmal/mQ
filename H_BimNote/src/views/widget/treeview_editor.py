import tkinter as tk
from tkinter import messagebox

from src.core.fp_utils import *
from src.controllers.tree_data_navigator import TreeDataManager_treeview


class TreeviewEditor:
    def __init__(self, state, impl_treeview):
        self.impl_treeview = impl_treeview
        self.treeview = self.impl_treeview.treeview
        self.tree = self.treeview.tree
        self.state = state
        self.entry_widget = None
        self.current_item = None
        self.current_column = None
        self.data_manager = TreeDataManager_treeview(state)

        # Bind double-click to initiate edit
        self.tree.bind("<Double-1>", self.on_double_click)

    def enable_edit(self):
        # Bind double-click to initiate edit
        self.tree.bind("<Double-1>", self.on_double_click)

    def disable_edit(self):
        self.tree.unbind("<Double-1>")

    def on_double_click(self, event):
        # Identify the column and item that was double-clicked
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not item_id or not column:
            return

        self.current_item = item_id
        self.current_column = int(column.replace("#", "")) - 1

        # Get the current value of the selected item
        current_values = self.tree.item(item_id, "values")
        if self.current_column >= len(current_values):
            # If the column index exceeds current values length, set current_value to empty
            current_value = ""
        else:
            current_value = current_values[self.current_column]

        # Create an Entry widget for editing
        bbox = self.tree.bbox(item_id, column)
        if not bbox:
            print("Error: Bounding box could not be determined")
            return

        x, y, width, height = bbox
        if width <= 0 or height <= 0:
            print("Error: Bounding box width or height is invalid")
            return

        self.entry_widget = tk.Entry(self.tree, width=width)
        self.entry_widget.place(x=x, y=y, width=width, height=height)
        self.entry_widget.insert(0, current_value)
        # self.entry_widget.grab_set()
        self.entry_widget.focus()

        # Bind events for Entry widget
        self.entry_widget.bind("<Return>", self.on_edit_complete)
        self.entry_widget.bind("<Escape>", self.on_edit_cancel)
        self.tree.bind("<MouseWheel>", self.on_edit_cancel)
        self.entry_widget.bind("<FocusOut>", self.on_edit_complete)

    def on_scroll(self, event):
        """Ask the user whether to cancel editing when they scroll."""
        if self.entry_widget:
            response = messagebox.askyesno(
                "Cancel Edit", "Do you want to cancel editing?"
            )
            if response:
                self.on_edit_cancel(None)

    def on_edit_complete(self, event):
        if self.current_item is None or self.current_column is None:
            return

        # Get the updated value from the Entry widget
        new_value = self.entry_widget.get()

        # Calc-Dict 자동 업데이트
        if self.current_column == 8 and new_value.startswith("Q"):
            std_calcdict = self.state.team_std_info["std-calcdict"]["children"]
            calcdict_nums = go(
                std_calcdict,
                map(lambda x: x["name"]),
                list,
            )
            if new_value not in calcdict_nums:
                std_calcdict.append(
                    {
                        "name": new_value,
                        "values": [new_value],
                        "children": [],
                    }
                )

        # Update the state with the new value using TreeDataManager
        selected_name = self.tree.item(self.current_item, "text")
        parent_path = self.get_item_path(self.current_item)
        self.data_manager.update_node_value(
            data_kind=self.impl_treeview.data_kind,
            path=parent_path,
            column_index=self.current_column,
            new_value=new_value,
        )

        # If the modified column matches the level depth, update the name as well
        depth = self.get_item_depth(self.current_item)
        if self.current_column == depth:
            self.data_manager.update_node_name(
                data_kind=self.impl_treeview.data_kind,
                path=parent_path,
                new_name=new_value,
            )

        # Notify observers that the state has been updated
        self.state.observer_manager.notify_observers(self.state)

        # Destroy the Entry widget
        self.entry_widget.destroy()
        self.entry_widget = None

    def on_edit_cancel(self, event):
        # Cancel editing and destroy the Entry widget
        if self.entry_widget:
            self.entry_widget.destroy()
            self.entry_widget = None

        self.tree.unbind("<MouseWheel>")
        # self.state.on_level_selected(None)

    def get_item_depth(self, item_id):
        """Calculate the depth of the given item in the tree."""
        depth = 0
        parent_id = self.tree.parent(item_id)
        while parent_id:
            depth += 1
            parent_id = self.tree.parent(parent_id)
        return depth

    def get_item_path(self, item_id):
        """Get the path of the given item from the root to the item."""
        path = []
        current_id = item_id
        while current_id:
            path.insert(0, self.tree.item(current_id, "text"))
            current_id = self.tree.parent(current_id)
        return path


class TreeviewEditor_stdGWMSWM(TreeviewEditor):
    def on_edit_complete(self, event):
        if self.current_item is None or self.current_column is None:
            return

        print(f"트리뷰수정이벤트::{event}")
        # Get the updated value from the Entry widget
        new_value = self.entry_widget.get()

        # Calc-Dict 자동 업데이트
        if self.current_column == 8 and new_value.startswith("Q"):
            std_calcdict = self.state.team_std_info["std-calcdict"]["children"]
            calcdict_nums = go(
                std_calcdict,
                map(lambda x: x["name"]),
                list,
            )
            if new_value not in calcdict_nums:
                std_calcdict.append(
                    {
                        "name": new_value,
                        "values": [new_value],
                        "children": [],
                    }
                )

        # Update the state with the new value using TreeDataManager
        selected_name = self.tree.item(self.current_item, "text")
        parent_path = self.get_item_path(self.current_item)
        self.data_manager.update_node_value(
            data_kind=self.impl_treeview.data_kind,
            path=parent_path,
            column_index=self.current_column,
            new_value=new_value,
        )

        # If the modified column matches the level depth, update the name as well
        depth = self.get_item_depth(self.current_item)
        if self.current_column == depth:
            self.data_manager.update_node_name(
                data_kind=self.impl_treeview.data_kind,
                path=parent_path,
                new_name=new_value,
            )

        # Update the GWM/SWM item name in std-familylist
        print("손잭스")
        self.impl_treeview.update_editing_stdType_wmItem_in(new_value)

        # Notify observers that the state has been updated
        self.state.observer_manager.notify_observers(self.state)

        # Destroy the Entry widget
        self.entry_widget.destroy()
        self.entry_widget = None


class TreeviewEditor_forAssignTreeview(TreeviewEditor):

    def on_edit_complete(self, event):
        if self.current_item is None or self.current_column is None:
            return

        # Get the updated value from the Entry widget
        new_value = self.entry_widget.get()

        # Update the state with the new value using TreeDataManager
        selected_name = self.tree.item(self.current_item, "text")
        parent_path = self.get_item_path(self.current_item)
        self.data_manager.update_node_value(
            data_kind=self.impl_treeview.data_kind,
            path=parent_path,
            column_index=self.current_column,
            new_value=new_value,
        )

        # If the modified column matches the level depth, update the name as well
        depth = self.get_item_depth(self.current_item)
        if self.current_column == depth:
            self.data_manager.update_node_name(
                data_kind=self.impl_treeview.data_kind,
                path=parent_path,
                new_name=new_value,
            )

        # Notify observers that the state has been updated
        self.state.observer_manager.notify_observers(self.state)

        # Destroy the Entry widget
        self.entry_widget.destroy()
        self.entry_widget = None

        # self.state.on_level_selected(None)
        try:
            self.impl_treeview.place_selected_item_at_top()
        except:
            pass


class TreeviewEditor_forBuildingList(TreeviewEditor):

    def on_edit_complete(self, event):
        if self.current_item is None or self.current_column is None:
            return

        # Get the updated value from the Entry widget
        new_value = self.entry_widget.get()

        # Update the state with the new value using TreeDataManager
        selected_name = self.tree.item(self.current_item, "text")
        parent_path = self.get_item_path(self.current_item)
        self.data_manager.update_node_value(
            data_kind=self.impl_treeview.data_kind,
            path=parent_path,
            column_index=self.current_column,
            new_value=new_value,
        )

        # If the modified column matches the level depth, update the name as well
        depth = self.get_item_depth(self.current_item)
        if self.current_column == depth:
            self.data_manager.update_node_name(
                data_kind=self.impl_treeview.data_kind,
                path=parent_path,
                new_name=new_value,
            )

        # state의 project-assigntype의 데이터 변경 반영
        data = self.state.team_std_info["project-assigntype"]["children"]
        for dic in data:
            if dic["values"][1] == selected_name:
                dic["values"][1] = new_value

        # Notify observers that the state has been updated
        self.state.observer_manager.notify_observers(self.state)

        # Destroy the Entry widget
        self.entry_widget.destroy()
        self.entry_widget = None

        # self.state.on_level_selected(None)
        try:
            self.impl_treeview.place_selected_item_at_top()
        except:
            pass
