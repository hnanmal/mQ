# src/views/widget/treeview_utils.py
from src.controllers.tree_data_navigator import TreeDataManager_treeview
from src.core.fp_utils import *
import tkinter as tk
from tkinter import (
    # ttk,
    simpledialog,
    messagebox,
)
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from src.views.widget.treeview_editor import TreeviewEditor
from src.views.widget.widget import StateObserver


# Composition for Style Management
class DefaultTreeViewStyleManager:

    @staticmethod
    def apply_style(treeview):
        style = ttk.Style()
        style.configure(
            # "Treeview",
            "Treeview",
            font=("Arial Narrow", 10),
            highlightthickness=1,
            background="white",
            foreground="black",
            rowheight=30,
            # height=50,
            height=20,
        )
        style.map(
            "Treeview",
            background=[("selected", "#fffec0")],  # Set the selection background color
            foreground=[("selected", "blue")],
        )  # Set the selection foreground color
        # Configure hover style
        style.configure(
            "Hover.Treeview", background="#d3d3d3", padding=(2, 2)
        )  # Light gray hover color
        style.configure("Treeview.Heading", font=("Arial Narrow", 10, "normal"))
        treeview.configure(style="Treeview")

    @staticmethod
    def apply_locked_style(treeview):
        style = ttk.Style()
        style.configure(
            "Custom_locked.Treeview",
            font=("Arial Narrow", 10),
            highlightthickness=1,
            background="#fafafa",
            foreground="black",
            height=50,
        )
        style.map(
            "Custom_locked.Treeview",
            background=[("selected", "#fffec0")],  # Set the selection background color
            foreground=[("selected", "blue")],
        )  # Set the selection foreground color
        # Configure hover style
        style.configure(
            "Hover.Custom_locked.Treeview", background="#d3d3d3", padding=(2, 2)
        )  # Light gray hover color
        style.configure(
            "Custom_locked.Treeview.Heading", font=("Arial Narrow", 10, "normal")
        )
        treeview.configure(style="Custom_locked.Treeview")

    @staticmethod
    def apply_alternate_row_colors(treeview):
        """Apply alternate row colors to the Treeview."""
        for i, item in enumerate(treeview.get_children("")):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            treeview.item(item, tags=(tag,))
            DefaultTreeViewStyleManager.apply_alternate_row_colors_recursive(
                treeview, item, i % 2 == 0
            )

        treeview.tag_configure("evenrow", background="white")
        treeview.tag_configure("oddrow", background="lightgray")

    @staticmethod
    def apply_alternate_row_colors_recursive(tree, item, is_even):
        """Apply alternate row colors recursively to child items."""
        children = tree.get_children(item)
        for i, child in enumerate(children):
            tag = (
                "evenrow"
                if (is_even and i % 2 == 0) or (not is_even and i % 2 != 0)
                else "oddrow"
            )
            tree.item(child, tags=(tag,))
            DefaultTreeViewStyleManager.apply_alternate_row_colors_recursive(
                tree, child, tag == "evenrow"
            )

    @staticmethod
    def apply_dynamic_alternate_row_colors(treeview):
        """현재 보이는 항목 기준으로 교차 색상을 적용"""
        visible_items = treeview.get_children("")  # 최상위 항목들 가져오기

        # 현재 보이는 모든 항목을 순회하는 함수
        def get_visible_items_recursively(items, result):
            for item in items:
                result.append(item)
                # 자식 항목 중 확장된 항목만 추가
                if treeview.item(item, "open"):  # 이 항목이 열려 있을 때만 자식 탐색
                    children = treeview.get_children(item)
                    if children:
                        get_visible_items_recursively(children, result)

        # 현재 트리뷰에서 보이는 모든 항목들을 가져옴
        all_visible_items = []
        get_visible_items_recursively(visible_items, all_visible_items)

        # 교차 색상 적용
        for i, item in enumerate(all_visible_items):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            treeview.item(item, tags=(tag,))

        # 태그에 대한 색상 정의
        treeview.tag_configure("evenrow", background="white")
        treeview.tag_configure("oddrow", background="#ebf0e6")


class ScrollbarWidget:
    def __init__(self, parent, target_widget, x=True, y=True):
        # self.frame = ttk.Frame(parent)
        self.frame = parent
        self.frame.pack(side="top", expand=True, fill="both")

        # The target widget should be provided by the user of this class.
        # self.target_widget = target_widget(self.frame)
        self.target_widget = target_widget

        commands_scroll = []
        if y and x:
            # Add Vertical Scrollbar
            self.v_scrollbar = ttk.Scrollbar(
                self.frame, orient="vertical", command=self.target_widget.yview
            )
            self.v_scrollbar.pack(side="right", fill="y")
            commands_scroll.append(self.v_scrollbar.set)

            # Add Horizontal Scrollbar
            self.h_scrollbar = ttk.Scrollbar(
                self.frame, orient="horizontal", command=self.target_widget.xview
            )
            self.h_scrollbar.pack(side="bottom", fill="x")
            # self.h_scrollbar.pack(fill="x")
            commands_scroll.append(self.h_scrollbar.set)
        elif y and not x:
            # Add Vertical Scrollbar
            self.v_scrollbar = ttk.Scrollbar(
                self.frame, orient="vertical", command=self.target_widget.yview
            )
            # self.v_scrollbar.pack(side="right", fill="y", anchor="ne")
            commands_scroll.append(self.v_scrollbar.set)
        elif not y and x:
            # Add Horizontal Scrollbar
            self.h_scrollbar = ttk.Scrollbar(
                self.frame, orient="horizontal", command=self.target_widget.xview
            )
            # self.h_scrollbar.pack(side="bottom", fill="x", anchor="sw")
            # self.h_scrollbar.pack(fill="x")
            commands_scroll.append(self.h_scrollbar.set)
        else:
            pass

        # Attach scrollbars to the target widget
        if commands_scroll:
            argNames = ["yscrollcommand", "xscrollcommand"]
            args = dict(zip(argNames, commands_scroll))
            self.target_widget.configure(
                **args
                # yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set
            )


class TreeViewContextMenu:
    def __init__(self, state, treeview, data_kind, **funcs):
        self.state = state
        self.treeview = treeview
        self.locked_status = None
        self.data_kind = data_kind
        self.funcs = funcs
        # Create the context menu
        self.menu = ttk.Menu(self.treeview.tree, tearoff=0)
        self.menu.add_command(label="Add Top Item", command=self.add_top_item)
        self.menu.add_command(label="Add Item", command=self.add_item)
        # self.menu.add_command(label="Edit Item", command=self.edit_item)
        self.menu.add_command(label="Delete Item", command=self.delete_item)
        if "copy_GWM" in funcs:
            self.menu.add_command(label="GWM항목 복사", command=self.copy_GWM)
        elif "copy_SWM" in funcs:
            self.menu.add_command(label="SWM항목 복사", command=self.copy_SWM)
        # Bind the right-click to show the menu
        self.treeview.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        # Debug statement to check locked status
        self.state.log_widget.write(f"Context Menu Locked Status: {self.locked_status}")
        # Only show the context menu if locked_status is False (unlocked)
        if not self.locked_status:
            # Get the item under the right-click
            item = self.treeview.tree.identify_row(event.y)
            if item:
                # Select the item that was right-clicked
                self.treeview.tree.selection_set(item)
                # Show the menu at the mouse position
                self.menu.post(event.x_root, event.y_root)

    def set_locked_status(self, status):
        """Setter to update the locked status."""
        self.locked_status = status
        self.state.log_widget.write(f"Locked Status Updated: {self.locked_status}")

    def copy_GWM(self):
        func = self.funcs.get("copy_GWM")
        func()

    def copy_SWM(self):
        func = self.funcs.get("copy_SWM")
        func()

    def add_top_item(self):
        func = self.funcs.get("add_top")
        func()

    def add_item(self):
        func = self.funcs.get("add")
        func()

    def edit_item(self):
        func = lambda: self.funcs.get("edit")
        func()

    def delete_item(self):
        func = self.funcs.get("delete")
        func()


class BaseTreeView:
    def __init__(self, state, parent, headers):
        self.state = state
        self.tree = ttk.Treeview(parent, columns=headers, show="headings")
        # self.tree = Tableview(parent, columns=headers, show="headings")
        self.setup_columns(headers)
        self.parent = parent

        # Configure tag styles
        self.tree.tag_configure(
            "hover",
            background="#d3d3d3",
            foreground="blue",
            font=("Arial Narrow", 10, "bold"),
            # padding=(2, 2),
        )  # Light gray background for hover

        self.tree.tag_configure(
            "normal", font=("Arial Narrow", 10)
        )  # Default white background

        # Track the last selected item
        self.last_selected_item = None

        # # 이벤트 바인딩
        # self.tree.bind(
        #     "<Motion>", self.on_mouse_motion
        # )  # 마우스 움직임을 감지해 hover 효과 적용
        # self.tree.bind(
        #     "<Leave>", self.on_mouse_leave
        # )  # 트리뷰에서 마우스가 나갔을 때 hover 효과 제거

    # 모든 항목에서 hover 효과 제거 함수 (재귀적으로 모든 하위 항목 포함)
    def clear_all_hover(self, tree):
        def clear_tags_recursive(item):
            if self.last_selected_item == item:
                children = tree.get_children(item)
                for child in children:
                    clear_tags_recursive(child)
            else:
                # 현재 항목의 태그를 'normal'로 변경
                tree.item(item, tags=("normal",))
                # 자식 항목들에 대해서도 동일하게 적용
                children = tree.get_children(item)
                for child in children:
                    clear_tags_recursive(child)

        # 루트 항목부터 시작하여 모든 항목에 대해 재귀적으로 태그 설정
        for root_item in tree.get_children():
            clear_tags_recursive(root_item)

    # Function to apply hover effect
    def on_mouse_motion(self, event):
        # 모든 항목의 hover 상태 초기화
        self.clear_all_hover(self.tree)
        # self.tree.config(cursor="circle")  # Change to a hand cursor

        # 마우스 커서 아래에 있는 아이템의 ID 가져오기
        item_id = self.tree.identify_row(event.y)
        if item_id:
            # hover 상태를 적용
            self.tree.item(item_id, tags=("hover",))

    # Function to reset all tags when the mouse leaves the widget
    def on_mouse_leave(self, event):
        self.clear_all_hover(self.tree)
        # self.tree.config(cursor="")  # Reset to default

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

    def prevent_expansion(self, event):
        # Prevent expansion or collapsing based on the lock state
        if self.locked:
            item_id = self.tree.focus()
            self.tree.item(item_id, open=False)

    def toggle_tree_lock(self, lock=True):
        """Locks or unlocks the tree from being expanded."""
        self.locked = lock
        if self.locked:
            self.tree.bind("<<TreeviewOpen>>", self.prevent_expansion)
            self.tree.bind("<<TreeviewClose>>", self.prevent_expansion)
        else:
            self.tree.unbind("<<TreeviewOpen>>")
            self.tree.unbind("<<TreeviewClose>>")

    def collapse_all_items(self):
        """Recursively collapse all items in the Treeview."""

        def collapse_item(item):
            # Set the item to closed (collapsed)
            self.tree.item(item, open=False)
            # Get the children of the current item
            children = self.tree.get_children(item)
            for child in children:
                collapse_item(child)

        # Get all root items
        root_items = self.tree.get_children("")
        for item in root_items:
            collapse_item(item)

    def expand_all_items(self):
        """Recursively expand all items in the Treeview."""
        treeview = self.tree
        self.collapse_all_items()

        def expand_item(item):
            self.state.log_widget.write(f"Expanding item: {item}")
            treeview.item(item, open=True)
            # Get the children of the current item
            children = treeview.get_children(item)
            for child in children:
                expand_item(child)

        # Get all root items
        root_items = treeview.get_children("")
        if not root_items:
            self.state.log_widget.write("No root items found.")
        for item in root_items:
            expand_item(item)

    def expand_tree_to_level(self, level):
        """Expand the treeview up to a given level."""
        # First, collapse all items to ensure fresh expansion
        self.collapse_all_items()

        def expand_item(item, current_level):
            # If the current level exceeds the specified level, stop expanding
            if current_level > level:
                return
            # Try to expand the current item
            try:
                self.tree.item(item, open=True)
                children = self.tree.get_children(item)
                for child in children:
                    expand_item(child, current_level + 1)
            except Exception as e:
                self.state.log_widget.write(
                    f"Error expanding tree at level {current_level}: {e}"
                )

        # Expand all root items initially
        root_items = self.tree.get_children("")
        for root in root_items:
            expand_item(root, 1)

    def remove_items_with_rule(self, data_list, _depth, _rule):
        """
        Removes items with an underscore in their 'name' at depth 2, along with their children.

        Parameters:
            data_list (list): A list of hierarchical data structures.

        Returns:
            list: Cleaned data with specified items removed.
        """

        def clean_children(children, depth):
            cleaned_children = []
            for child in children:
                # At depth 2, check for underscores in the 'name' field
                if depth == _depth and _rule in child.get("name", ""):
                    continue  # Skip this item and its children
                # Recursively clean if 'children' field exists
                if "children" in child:
                    child["children"] = clean_children(child["children"], depth + 1)
                cleaned_children.append(child)
            return cleaned_children

        # Process each top-level item in the list
        for item in data_list:
            if "children" in item:
                item["children"] = clean_children(item["children"], _depth)

        return data_list

    def insert_data_with_levels(self, data, parent_id=""):
        """Insert data into the TreeView with levels based on the new data structure."""
        for node in data:
            if isinstance(node, dict):
                # Extract the last value in the 'values' list to be displayed in the TreeView
                # display_value = node["values"][-1] if node["values"] else ""
                display_value = node["values"]

                # Insert the current node with its name and the last value from 'values'
                node_id = self.tree.insert(
                    parent_id, "end", text=node["name"], values=(display_value)
                )
                self.tree.item(
                    node_id,  # open=True
                )  # Keep the tree open to display all items

                # Recursively insert children if there are any
                if "children" in node and isinstance(node["children"], list):
                    self.insert_data_with_levels(node["children"], node_id)

            elif isinstance(node, str):
                # Insert the string as a leaf node without additional children
                # self.tree.insert(parent_id, "end", text=node, values=(node,))
                pass

    def get_item_indices(self, selected_item_id):
        indices = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.tree.parent(current_item)
            siblings = self.tree.get_children(parent_id)

            try:
                # Get the index of the current item among its siblings
                item_index = siblings.index(current_item)
            except ValueError:
                # If the item is not found among siblings, there's an issue
                self.state.log_widget.write(
                    f"Error: Item '{current_item}' not found among siblings {siblings}"
                )
                return []

            # Debug: print current processing details
            self.state.log_widget.write(
                f"Current item: {current_item}, Parent ID: {parent_id}, Index: {item_index}"
            )

            # Insert the item index at the beginning of the list to maintain top-down order
            indices.insert(0, item_index)

            # Move to the parent item
            current_item = parent_id

        # Debug: print the final indices
        self.state.log_widget.write(f"Final Indices: {indices}")
        return indices

    def select_item_by_indices(self, indices):
        """
        Select an item in the Treeview using the provided indices.
        """
        current_parent = ""
        target_item = None

        for index in indices:
            children = self.tree.get_children(current_parent)
            if index < len(children):
                target_item = children[index]
                current_parent = target_item
            else:
                self.state.log_widget.write(
                    f"Index {index} is out of bounds for the current parent."
                )
                return

        if target_item:
            self.tree.selection_set(target_item)
            self.tree.focus(target_item)
            self.tree.see(target_item)


class TeamStd_GWMTreeView:
    def __init__(self, state, parent, showmode="team", view_level=2):
        self.state = state
        self.data_kind = "std-GWM"
        self.showmode = showmode
        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.state_observer = StateObserver(state, lambda e: self.update(e, view_level))

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "G-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Create and integrate context menu
        self.context_menu = TreeViewContextMenu(
            state,
            self.treeview,
            data_kind=self.data_kind,
            add_top=self.add_top_item,
            add=self.add_item,
            delete=self.delete_item,
            copy_GWM=self.copy_GWM,
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(parent, text="Standard Types for GWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None, view_level=None):
        state = self.state
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")

        selected_item_id = self.treeview.tree.focus()
        origin_indices = None

        # Extract origin indices if a valid item is focused
        if selected_item_id:
            try:
                origin_indices = self.treeview.get_item_indices(selected_item_id)
                print(origin_indices, "!!!")
            except Exception as e:
                print(f"origin_indices 추출 실패: {e}")

        """Update the TreeView whenever the state changes."""
        if self.data_kind in state.team_std_info:
            if self.showmode == "team":
                data = self.treeview.remove_items_with_rule(
                    state.team_std_info[self.data_kind]["children"],
                    _depth=2,
                    _rule="::",
                )
                # data = state.team_std_info[self.data_kind]["children"]
            else:
                data = state.team_std_info[self.data_kind]["children"]

            # Clear the TreeView and reload data from the updated state
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

            self.treeview.expand_tree_to_level(level=view_level)
        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                self.state.log_widget.write(f"Item selection failed: {e}")

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        treeDataManager = TreeDataManager_treeview(self.state)
        try:
            # Reset the tag for the previously selected item to 'normal'
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            self.state.log_widget.write(f"Error resetting last selected item tag: {e}")

        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        self.treeview.last_selected_item = selected_item_id

        try:
            state_data = self.state.team_std_info[self.data_kind]["children"]
            target_node = treeDataManager.find_node_by_name_recur(
                state_data, self.treeview.tree.item(selected_item_id, "text")
            ).copy()
            self.state.log_widget.write(
                f"select tree item!!! {self.treeview.tree.item(selected_item_id, 'text')}"
            )

            self.state.selectedGWMitems = [target_node]
        except:
            pass

        # Get the parent and grandparent of the selected item
        parent_item_id = self.treeview.tree.parent(selected_item_id)
        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)

        # Extract the names from the values, ensuring each level is handled appropriately
        try:
            # Get the name of the selected item, parent, and grandparent
            selected_item_name = go(
                self.treeview.tree.item(selected_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )
            parent_item_name = go(
                self.treeview.tree.item(parent_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )
            grand_parent_item_name = go(
                self.treeview.tree.item(grand_parent_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )

            # Format the selected path as "grandparent | parent | selected"
            formatted_value = " | ".join(
                filter(
                    None, [grand_parent_item_name, parent_item_name, selected_item_name]
                )
            )

            # Update the selected item in the state
            self.selected_item.set(formatted_value)

            # Register the last selected item
            self.last_selected_item = selected_item_id

        except Exception as e:
            self.state.log_widget.write(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        self.state.log_widget.write(
            f"Parent IDs for selected item '{selected_item_id}': {parent_ids}"
        )
        return list(reversed(parent_ids))

    def copy_GWM(self):
        state = self.state

        selected_item_id = self.treeview.tree.selection()
        selected_item_name = go(
            selected_item_id,
            lambda x: self.treeview.tree.item(x, "values"),
            filter(lambda x: x != ""),
            list,
        )[0]
        new_name = selected_item_name + "::copy"

        parent_item_id = self.treeview.tree.parent(selected_item_id)
        if parent_item_id:
            parent_item_name = go(
                parent_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
        else:
            parent_item_name = ""

        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)
        if grand_parent_item_id:
            grand_parent_item_name = go(
                grand_parent_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
        else:
            grand_parent_item_name = ""

        path = go(
            [grand_parent_item_name, parent_item_name, selected_item_name],
            filter(lambda x: x != ""),
            list,
        )
        print(f"path: {path}")

        self.treeDataManager.copy_node(
            data_kind=self.data_kind,
            path=path,
            new_name=new_name,
            name_depth=1,
        )
        state.observer_manager.notify_observers(state)

    def add_top_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Top Item", "Enter the name of the new item:"
        )
        if new_item_name:
            self.treeDataManager.add_top_level_node(self.data_kind, new_item_name)
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def add_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Item", "Enter the name of the new item:"
        )
        if new_item_name:
            selected_item_id = self.treeview.tree.selection()
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
            self.treeDataManager.add_child_node(
                self.data_kind, selected_item_name, new_item_name
            )
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state

        # Get the selected item ID
        selected_item_id = self.treeview.tree.selection()
        if not selected_item_id:
            print("No item selected.")
            return
        selected_item_id = selected_item_id[0]  # Handle single selection case

        # Build the full path to the selected item
        def get_full_path(item_id):
            path = []
            current_item_id = item_id
            while current_item_id:
                # Get the name of the current item
                item_values = self.treeview.tree.item(current_item_id, "values")
                item_name = next(
                    (v for v in item_values if v), None
                )  # Get the first non-empty value
                if item_name:
                    path.insert(0, item_name)  # Add to the beginning of the path
                # Move to the parent item
                current_item_id = self.treeview.tree.parent(current_item_id)
            return path

        # Get the full path of the selected item
        full_path = get_full_path(selected_item_id)
        print(f"Deleting item with path: {full_path}")

        # Validate the constructed path
        if not full_path:
            print("Could not construct a valid path for the selected item.")
            return

        # Pass the full path to the delete_node method
        try:
            self.treeDataManager.delete_node(self.data_kind, full_path)
            print(f"Successfully deleted item with path: {full_path}")
        except Exception as e:
            print(f"Error deleting item with path {full_path}: {e}")

        # Notify observers about the state update
        state.observer_manager.notify_observers(state)


class PjtStd_GWMTreeView(TeamStd_GWMTreeView):
    def __init__(self, state, parent):
        super().__init__(state, parent, view_level=2)


class TeamStd_WMmatching_TreeView:
    def __init__(self, state, parent, relate_widget, data_kind=None, view_level=2):
        self.state = state
        self.data_kind = data_kind
        self.selected_item_relate_widget = relate_widget.selected_item
        headers = ["Work Master"]
        hdr_widths = [1000]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)
        self.state_observer = StateObserver(state, lambda e: self.update(e, view_level))

        # config selection mode
        self.treeview.tree.config(selectmode="extended")

        # Tag styles
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(
            parent, text="Matched WMs for Selected Standard Types", font=title_font
        )
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None, view_level=None):
        state = self.state
        """Update the TreeView whenever the state changes."""
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        self.state.log_widget.write(
            f"선택아이템 출력 : {self.selected_item_relate_widget.get()}"
        )

        try:
            # Split the selected item path to find the grandparent, parent, and selected item names
            grand_parent_item_name, parent_item_name, selected_item_name = (
                self.selected_item_relate_widget.get().split(" | ")
            )

            # Ensure the data kind exists in the team standard information
            if self.data_kind in state.team_std_info:
                data = state.team_std_info[self.data_kind]["children"]

                # Find the grandparent node
                grand_parent_node = next(
                    (node for node in data if node["name"] == grand_parent_item_name),
                    None,
                )
                if grand_parent_node:
                    # Find the parent node
                    parent_node = next(
                        (
                            node
                            for node in grand_parent_node["children"]
                            if node["name"] == parent_item_name
                        ),
                        None,
                    )
                    if parent_node:
                        # Find the selected node
                        selected_node = next(
                            (
                                node
                                for node in parent_node["children"]
                                if node["name"] == selected_item_name
                            ),
                            None,
                        )
                        if selected_node:
                            # Clear the TreeView and insert the data for the selected node
                            self.treeview.clear_treeview()

                            # Wrap the children of the selected node for insertion
                            wrapped_data = go(
                                selected_node["children"],
                                map(lambda x: [x]),
                                list,
                            )
                            # self.treeview.insert_data_with_levels(wrapped_data)
                            self.treeview.insert_data(wrapped_data)
                        else:
                            self.state.log_widget.write(
                                f"Selected item '{selected_item_name}' not found."
                            )
                    else:
                        self.state.log_widget.write(
                            f"Parent item '{parent_item_name}' not found."
                        )
                else:
                    self.state.log_widget.write(
                        f"Grandparent item '{grand_parent_item_name}' not found."
                    )

        except Exception as e:
            self.state.log_widget.write(
                f"{self.__class__.__name__} > update 메소드 진입 안됩니다~: {e}"
            )

        self.treeview.expand_tree_to_level(level=view_level)

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        # if self.last_selected_item:
        #     self.treeview.tree.item(self.treeview.last_selected_item, tags=("normal",))

        self.state.log_widget.write("on_item_selected_시작")
        selected_items_id = self.treeview.tree.selection()
        selected_items_name = go(
            selected_items_id,
            map(lambda x: list(self.treeview.tree.item(x, "values"))),
            list,
            map(lambda x: x[0]),
            list,
        )
        # print(selected_items_name)
        self.state.selected_matchedWMs = selected_items_name
        # # 마지막 선택항목으로 재등록
        # self.last_selected_item = selected_items_id[0]
        self.state.log_widget.write("on_item_selected_종료")


class TeamStd_SWMTreeView:
    def __init__(self, state, parent, showmode="team", view_level=2):
        self.state = state
        self.data_kind = "std-SWM"
        self.showmode = showmode
        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.state_observer = StateObserver(state, lambda e: self.update(e, view_level))

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        # headers = ["분류", "S-WM", "Item"]
        headers = ["분류-1", "분류-2", "S-WM"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Create and integrate context menu
        self.context_menu = TreeViewContextMenu(
            state,
            self.treeview,
            self.data_kind,
            add_top=self.add_top_item,
            add=self.add_item,
            delete=self.delete_item,
            copy_SWM=self.copy_SWM,
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(parent, text="Standard Types for SWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None, view_level=None):
        state = self.state
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")

        selected_item_id = self.treeview.tree.focus()
        origin_indices = None

        # Extract origin indices if a valid item is focused
        if selected_item_id:
            try:
                origin_indices = self.treeview.get_item_indices(selected_item_id)
                print(origin_indices, "!!!")
            except Exception as e:
                print(f"origin_indices 추출 실패: {e}")

        """Update the TreeView whenever the state changes."""
        if self.data_kind in state.team_std_info:
            if self.showmode == "team":
                data = self.treeview.remove_items_with_rule(
                    state.team_std_info[self.data_kind]["children"],
                    _depth=2,
                    _rule="::",
                )
            else:
                data = state.team_std_info[self.data_kind]["children"]

            # Clear the TreeView and reload data from the updated state
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

            self.treeview.expand_tree_to_level(level=view_level)

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                print(f"Item selection failed: {e}")

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        treeDataManager = TreeDataManager_treeview(self.state)
        try:
            # Reset the tag for the previously selected item to 'normal'
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            self.state.log_widget.write(f"Error resetting last selected item tag: {e}")

        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        self.treeview.last_selected_item = selected_item_id

        try:
            state_data = self.state.team_std_info[self.data_kind]["children"]
            target_node = treeDataManager.find_node_by_name_recur(
                state_data, self.treeview.tree.item(selected_item_id, "text")
            ).copy()
            self.state.log_widget.write(
                f"select tree item!!! {self.treeview.tree.item(selected_item_id, 'text')}"
            )

            self.state.selectedGWMitems = [target_node]
        except:
            pass

        # Get the parent and grandparent of the selected item
        parent_item_id = self.treeview.tree.parent(selected_item_id)
        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)

        # Extract the names from the values, ensuring each level is handled appropriately
        try:
            # Get the name of the selected item, parent, and grandparent
            selected_item_name = go(
                self.treeview.tree.item(selected_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )
            parent_item_name = go(
                self.treeview.tree.item(parent_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )
            grand_parent_item_name = go(
                self.treeview.tree.item(grand_parent_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )

            # Format the selected path as "grandparent | parent | selected"
            formatted_value = " | ".join(
                filter(
                    None, [grand_parent_item_name, parent_item_name, selected_item_name]
                )
            )

            # Update the selected item in the state
            self.selected_item.set(formatted_value)

            # Register the last selected item
            self.last_selected_item = selected_item_id

        except Exception as e:
            self.state.log_widget.write(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        self.state.log_widget.write(
            f"Parent IDs for selected item '{selected_item_id}': {parent_ids}"
        )
        return list(reversed(parent_ids))

    def copy_SWM(self):
        state = self.state

        selected_item_id = self.treeview.tree.selection()
        selected_item_name = go(
            selected_item_id,
            lambda x: self.treeview.tree.item(x, "values"),
            filter(lambda x: x != ""),
            list,
        )[0]
        new_name = selected_item_name + "::copy"

        parent_item_id = self.treeview.tree.parent(selected_item_id)
        if parent_item_id:
            parent_item_name = go(
                parent_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
        else:
            parent_item_name = ""

        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)
        if grand_parent_item_id:
            grand_parent_item_name = go(
                grand_parent_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
        else:
            grand_parent_item_name = ""

        path = go(
            [grand_parent_item_name, parent_item_name, selected_item_name],
            filter(lambda x: x != ""),
            list,
        )
        print(f"path: {path}")

        self.treeDataManager.copy_node(
            data_kind=self.data_kind,
            path=path,
            new_name=new_name,
            name_depth=2,
        )
        state.observer_manager.notify_observers(state)

    def add_top_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Top Item", "Enter the name of the new item:"
        )
        if new_item_name:
            self.treeDataManager.add_top_level_node(self.data_kind, new_item_name)
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def add_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Item", "Enter the name of the new item:"
        )
        if new_item_name:
            selected_item_id = self.treeview.tree.selection()
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
            self.treeDataManager.add_child_node(
                self.data_kind, selected_item_name, new_item_name
            )
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state

        # Get the selected item ID
        selected_item_id = self.treeview.tree.selection()
        if not selected_item_id:
            print("No item selected.")
            return
        selected_item_id = selected_item_id[0]  # Handle single selection case

        # Build the full path to the selected item
        def get_full_path(item_id):
            path = []
            current_item_id = item_id
            while current_item_id:
                # Get the name of the current item
                item_values = self.treeview.tree.item(current_item_id, "values")
                item_name = next(
                    (v for v in item_values if v), None
                )  # Get the first non-empty value
                if item_name:
                    path.insert(0, item_name)  # Add to the beginning of the path
                # Move to the parent item
                current_item_id = self.treeview.tree.parent(current_item_id)
            return path

        # Get the full path of the selected item
        full_path = get_full_path(selected_item_id)
        print(f"Deleting item with path: {full_path}")

        # Validate the constructed path
        if not full_path:
            print("Could not construct a valid path for the selected item.")
            return

        # Pass the full path to the delete_node method
        try:
            self.treeDataManager.delete_node(self.data_kind, full_path)
            print(f"Successfully deleted item with path: {full_path}")
        except Exception as e:
            print(f"Error deleting item with path {full_path}: {e}")

        # Notify observers about the state update
        state.observer_manager.notify_observers(state)

    # def delete_item(self):
    #     state = self.state

    #     selected_item_id = self.treeview.tree.selection()
    #     selected_item_name = go(
    #         selected_item_id,
    #         lambda x: self.treeview.tree.item(x, "values"),
    #         filter(lambda x: x != ""),
    #         list,
    #     )[0]
    #     parent_item_id = self.treeview.tree.parent(selected_item_id)
    #     parent_item_name = go(
    #         parent_item_id,
    #         lambda x: self.treeview.tree.item(x, "values"),
    #         filter(lambda x: x != ""),
    #         list,
    #     )[0]
    #     grand_parent_item_id = self.treeview.tree.parent(parent_item_id)
    #     grand_parent_item_name = go(
    #         grand_parent_item_id,
    #         lambda x: self.treeview.tree.item(x, "values"),
    #         filter(lambda x: x != ""),
    #         list,
    #     )[0]

    #     self.treeDataManager.delete_node(
    #         self.data_kind,
    #         # selected_item_name,
    #         [grand_parent_item_name, parent_item_name, selected_item_name],
    #     )
    #     # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
    #     state.observer_manager.notify_observers(state)


###################for common_input################################################################


class TeamStd_CommonInputTreeView:
    def __init__(self, state, parent, data_kind="common-input", view_level=2):
        self.state = state
        # self.data_kind = "common-input"
        self.data_kind = data_kind

        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.state_observer = StateObserver(state, lambda e: self.update(e, view_level))

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "Abbreviation", "Description", "Input", "Unit", "Remark"]
        hdr_widths = [127, 125, 200, 50, 50, 200]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)
        # self.add_item = self.treeviewEditor.add_item

        # Track the last selected item with an instance attribute
        self.last_selected_item = None

        # Bind selection events
        self.treeview.tree.bind(
            "<<TreeviewSelect>>", lambda e: self.on_item_selected(e)
        )

        # Create and integrate context menu
        self.context_menu = TreeViewContextMenu(
            state,
            self.treeview,
            data_kind=self.data_kind,
            add_top=self.add_top_item,
            add=self.add_item,
            delete=self.delete_item,
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(
            parent, text="Standard Common Input Setting", font=title_font
        )
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None, view_level=None):
        state = self.state
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")

        selected_item_id = self.treeview.tree.focus()
        origin_indices = None

        # Extract origin indices if a valid item is focused
        if selected_item_id:
            try:
                origin_indices = self.treeview.get_item_indices(selected_item_id)
                print(origin_indices, "!!!")
            except Exception as e:
                print(f"origin_indices 추출 실패: {e}")

        """Update the TreeView whenever the state changes."""
        if self.data_kind in state.team_std_info:
            # Clear the TreeView and reload data from the updated state
            data = state.team_std_info[self.data_kind]["children"]
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

            self.treeview.expand_tree_to_level(level=view_level)

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                self.state.log_widget.write(f"Item selection failed: {e}")

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        try:
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            self.state.log_widget.write(f"Error resetting last selected item tag: {e}")

        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        self.last_selected_item = selected_item_id

        # Get the parent of the selected item based on its structure
        parent_item_id = self.treeview.tree.parent(selected_item_id)

        try:
            # Extract the names from the values, ensuring each level is handled appropriately
            selected_values = self.treeview.tree.item(selected_item_id, "values")
            parent_values = self.treeview.tree.item(parent_item_id, "values")

            selected_item_name = next((v for v in selected_values if v), None)
            parent_item_name = next((v for v in parent_values if v), None)

            # Format the selected path as "parent | selected"
            formatted_value = " | ".join(
                filter(None, [parent_item_name, selected_item_name])
            )

            # Update the selected item in the state
            self.selected_item.set(formatted_value)

            # Register the last selected item
            self.last_selected_item = selected_item_id

        except IndexError as e:
            self.state.log_widget.write(f"IndexError: {e}")
        except Exception as e:
            self.state.log_widget.write(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        self.state.log_widget.write(
            f"Parent IDs for selected item '{selected_item_id}': {parent_ids}"
        )
        return list(reversed(parent_ids))

    def add_top_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Top Item", "Enter the name of the new item:"
        )
        if new_item_name:
            self.treeDataManager.add_top_level_node(self.data_kind, new_item_name)
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def add_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Item", "Enter the name of the new item:"
        )
        if new_item_name:
            selected_item_id = self.treeview.tree.selection()
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
            self.treeDataManager.add_child_node(
                self.data_kind, selected_item_name, new_item_name
            )
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state

        # Get the selected item ID
        selected_item_id = self.treeview.tree.selection()
        if not selected_item_id:
            print("No item selected.")
            return
        selected_item_id = selected_item_id[0]  # Handle single selection case

        # Build the full path to the selected item
        def get_full_path(item_id):
            path = []
            current_item_id = item_id
            while current_item_id:
                # Get the name of the current item
                item_values = self.treeview.tree.item(current_item_id, "values")
                item_name = next(
                    (v for v in item_values if v), None
                )  # Get the first non-empty value
                if item_name:
                    path.insert(0, item_name)  # Add to the beginning of the path
                # Move to the parent item
                current_item_id = self.treeview.tree.parent(current_item_id)
            return path

        # Get the full path of the selected item
        full_path = get_full_path(selected_item_id)
        print(f"Deleting item with path: {full_path}")

        # Validate the constructed path
        if not full_path:
            print("Could not construct a valid path for the selected item.")
            return

        # Pass the full path to the delete_node method
        try:
            self.treeDataManager.delete_node(self.data_kind, full_path)
            print(f"Successfully deleted item with path: {full_path}")
        except Exception as e:
            print(f"Error deleting item with path {full_path}: {e}")

        # Notify observers about the state update
        state.observer_manager.notify_observers(state)


################################


class TeamStd_FamlistTreeView:
    def __init__(self, state, parent, title="Standard Family List", view_level=2):
        self.state = state
        self.data_kind = "std-familylist"
        self.view_level = view_level
        self.title = title

        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.state_observer = StateObserver(state, lambda e: self.update(e, view_level))

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = [
            "최상위",
            "분류",
            "No",
            "Family Name",
            "GWM/SWM",
            "Item",
            "표준산출 수식",
            "Description",
            "표준산출유형 번호",
        ]
        hdr_widths = [0, 60, 20, 150, 100, 100, 100, 200, 50]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        tree_frame.pack()
        self.tree_frame = tree_frame

        # Add ComboBox for selecting view level
        self.level_combobox = ttk.Combobox(
            # tree_frame, values=list(range(1, len(headers) + 1)), state="readonly"
            tree_frame,
            values=list(range(1, 5)),
            state="readonly",
        )
        self.level_combobox.current(view_level - 1)  # Set default level
        self.level_combobox.bind("<<ComboboxSelected>>", self.on_level_selected)
        self.level_combobox.pack(pady=5)

        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # self.state.on_level_selected = self.on_level_selected

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)
        self.treeview.tree.column("GWM/SWM", anchor="center")  # Center-align

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        self.state.on_level_selected = self.on_level_selected

        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.treeview.tree.bind(
            "<<TreeviewOpen>>",
            DefaultTreeViewStyleManager.apply_dynamic_alternate_row_colors(
                self.treeview.tree
            ),
        )
        self.treeview.tree.bind(
            "<<TreeviewClose>>",
            DefaultTreeViewStyleManager.apply_dynamic_alternate_row_colors(
                self.treeview.tree
            ),
        )

        # Create and integrate context menu
        self.context_menu = TreeViewContextMenu(
            state,
            self.treeview,
            data_kind=self.data_kind,
            add_top=self.add_top_item,
            add=self.add_item,
            delete=self.delete_item,
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent, text=None):
        if not text:
            text = self.title
        title_font = ttk.font.Font(family="맑은 고딕", size=11)
        title_label = ttk.Label(parent, text=text, font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None, view_level=None):
        state = self.state
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")

        selected_item_id = self.treeview.tree.focus()
        origin_indices = None

        # Extract origin indices if a valid item is focused
        if selected_item_id:
            try:
                origin_indices = self.treeview.get_item_indices(selected_item_id)
                print(origin_indices, "!!!")
            except Exception as e:
                print(f"origin_indices 추출 실패: {e}")

        """Update the TreeView whenever the state changes."""
        if self.data_kind in state.team_std_info:
            # Clear the TreeView and reload data from the updated state
            data = state.team_std_info[self.data_kind]["children"]
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

            self.treeview.expand_tree_to_level(level=view_level)

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                self.state.log_widget.write(f"Item selection failed: {e}")

        self.on_level_selected(event=None)

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        try:
            # # Reset the tag for the previously selected item to 'normal'
            # if self.last_selected_item:
            #     self.treeview.tree.item(self.last_selected_item, tags=("normal",))
            # 이전 선택 항목이 있었다면 원래 색상으로 복원
            if (
                self.last_selected_item
                and self.last_selected_item not in selected_item_id
            ):
                original_tag = self.treeview.item(self.last_selected_item, "tags")[0]
                self.treeview.item(self.last_selected_item, tags=(original_tag,))

            # 현재 선택된 항목의 스타일을 변경
            if selected_item_id:
                for item in selected_item_id:
                    self.treeview.item(item, tags=("selected",))
        except Exception as e:
            self.state.log_widget.write(f"Error resetting last selected item tag: {e}")

        self.treeview.last_selected_item = selected_item_id
        self.state.log_widget.write(
            f"select tree item!!! {self.treeview.tree.item(selected_item_id, 'text')}"
        )

        # Get the parent and grandparent of the selected item
        parent_item_id = self.treeview.tree.parent(selected_item_id)
        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)
        # Extract the names from the values, ensuring each level is handled appropriately
        try:
            # Get the name of the selected item, parent, and grandparent
            selected_item_name = go(
                self.treeview.tree.item(selected_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )
            parent_item_name = go(
                self.treeview.tree.item(parent_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0],
            )
            grand_parent_item_name = go(
                self.treeview.tree.item(grand_parent_item_id, "values"),
                filter(lambda x: x != ""),
                list,
                lambda x: x[0] or "",
            )

            # Format the selected path as "grandparent | parent | selected"
            formatted_value = " | ".join(
                filter(
                    # None, [grand_parent_item_name, parent_item_name, selected_item_name]
                    None,
                    [grand_parent_item_name, parent_item_name, selected_item_name],
                )
            )
            self.state.log_widget.write(
                f"패밀리리스트 선택 항목 포맷 밸류 {formatted_value}"
            )

            # Update the selected item in the state
            self.selected_item.set(formatted_value)
            self.state.log_widget.write(
                f"패밀리리스트 선택 항목 {self.selected_item.get()}"
            )
            # Register the last selected item
            self.last_selected_item = selected_item_id

        except Exception as e:
            self.state.log_widget.write(f"Error processing selected item details: {e}")

    def place_selected_item_at_top(self, tree):
        """Place the selected item at the top of the Treeview."""
        selected_item = tree.selection()
        if selected_item:
            # Get the index of the selected item
            index = tree.index(selected_item[0])

            # Calculate the fraction to scroll
            total_items = len(tree.get_children())
            if total_items > 0:
                fraction = index / total_items
                tree.yview_moveto(fraction)

    def on_level_selected(self, event):
        """Handle combo box selection and expand the tree to the selected level."""
        try:
            selected_level = int(self.level_combobox.get())
            self.treeview.expand_tree_to_level(level=selected_level)
            # 트리뷰 데이터를 갱신하거나 레벨을 변경한 후 호출
            DefaultTreeViewStyleManager.apply_dynamic_alternate_row_colors(
                self.treeview.tree
            )
            if self.treeview.tree.focus():
                selected_item = self.treeview.tree.focus()
                # print(selected_item)
                # self.treeview.tree.see(selected_item)
                self.place_selected_item_at_top(self.treeview.tree)

        except ValueError as e:
            self.state.log_widget.write(f"Invalid level selected: {e}")
        except Exception as e:
            self.state.log_widget.write(
                f"Error expanding tree to level {selected_level}: {e}"
            )

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        self.state.log_widget.write(
            f"Parent IDs for selected item '{selected_item_id}': {parent_ids}"
        )
        return list(reversed(parent_ids))

    def add_top_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Top Item", "Enter the name of the new item:"
        )
        if new_item_name:
            self.treeDataManager.add_top_level_node(self.data_kind, new_item_name)
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def add_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Item", "Enter the name of the new item:"
        )
        if new_item_name:
            selected_item_id = self.treeview.tree.selection()
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
            self.treeDataManager.add_child_node(
                self.data_kind, selected_item_name, new_item_name
            )
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state

        # Get the selected item ID
        selected_item_id = self.treeview.tree.selection()
        if not selected_item_id:
            print("No item selected.")
            return
        selected_item_id = selected_item_id[0]  # Handle single selection case

        # Build the full path to the selected item
        def get_full_path(item_id):
            path = []
            current_item_id = item_id
            while current_item_id:
                # Get the name of the current item
                item_values = self.treeview.tree.item(current_item_id, "values")
                item_name = next(
                    (v for v in item_values if v), None
                )  # Get the first non-empty value
                if item_name:
                    path.insert(0, item_name)  # Add to the beginning of the path
                # Move to the parent item
                current_item_id = self.treeview.tree.parent(current_item_id)
            return path

        # Get the full path of the selected item
        full_path = get_full_path(selected_item_id)
        print(f"Deleting item with path: {full_path}")

        # Validate the constructed path
        if not full_path:
            print("Could not construct a valid path for the selected item.")
            return

        # Pass the full path to the delete_node method
        try:
            self.treeDataManager.delete_node(self.data_kind, full_path)
            print(f"Successfully deleted item with path: {full_path}")
        except Exception as e:
            print(f"Error deleting item with path {full_path}: {e}")

        # Notify observers about the state update
        state.observer_manager.notify_observers(state)

    # def delete_item(self):
    #     state = self.state

    #     selected_item_id = self.treeview.tree.selection()
    #     selected_item_name = go(
    #         selected_item_id,
    #         lambda x: self.treeview.tree.item(x, "values"),
    #         filter(lambda x: x != ""),
    #         list,
    #     )[0]

    #     self.treeDataManager.delete_node(
    #         self.data_kind,
    #         selected_item_name,
    #     )
    #     # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
    #     state.observer_manager.notify_observers(state)


class TeamStd_calcDict_TreeView:
    def __init__(self, state, parent, relate_widget, data_kind=None, view_level=3):
        self.state = state
        # self.data_kind = data_kind
        self.data_kind = "std-calcdict"
        self.view_level = view_level
        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.state_observer = StateObserver(
            state, lambda e: self.update(event=e, view_level=self.view_level)
        )
        self.selected_item_relate_widget = relate_widget.selected_item
        headers = [
            "표준산출유형 번호",
            "심벌키",
            "심벌값",
            # "GWM/SWM",
            # "표준산출 수식",
        ]
        hdr_widths = [100, 50, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.add_update_button(tree_frame)
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="extended")

        # Tag styles
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        self.context_menu = TreeViewContextMenu(
            state,
            self.treeview,
            data_kind=self.data_kind,
            add_top=self.add_top_item,
            add=self.add_item,
            delete=self.delete_item,
        )

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(
            parent, text="Matched WMs for Selected Standard Types", font=title_font
        )
        title_label.pack(padx=5, pady=5, anchor="w")

    def add_update_button(self, parent):
        """Adds an Update button to the tree view."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=5)

        update_button = ttk.Button(
            button_frame,
            text="Update from common-input",
            command=lambda: self.update_target_byRef("common-input"),
        )
        update_button.pack(padx=10, side="left")

    def update_target_byRef(self, dbKey):
        state = self.state

        pattern = r"^\d+\.\d+$"
        selected_NoItem = go(
            self.selected_item_relate_widget.get().split(" | "),
            filter(lambda x: re.match(pattern, x)),
            next,
        )
        selected_qItem_name = f"Q{selected_NoItem}"
        # Ensure the data kind exists in the team standard information
        data = state.team_std_info[self.data_kind]["children"]
        selected_node = next(
            (node for node in data if node["name"] == selected_qItem_name),
            None,
        )
        # state.log_widget.write(str(selected_node))

        refData = state.team_std_info[dbKey]
        targetData = selected_node
        # Flatten A data into a dictionary with 'name' as key and 'values' as value
        a_values_map = {}

        def flatten_a_data(data):
            if isinstance(data, list):
                for item in data:
                    flatten_a_data(item)
            elif isinstance(data, dict):
                a_values_map[data["name"]] = data["values"]
                flatten_a_data(data.get("children", []))

        # Flatten A data for easy lookup
        flatten_a_data(refData["children"])

        # Update B data
        for child in targetData["children"]:
            if child["name"] in a_values_map:
                # Get the fourth value of the matched A data
                a_value_to_update = (
                    a_values_map[child["name"]][3]
                    if len(a_values_map[child["name"]]) > 3
                    else None
                )
                if a_value_to_update:
                    # Update the second value of B data
                    child["values"].insert(2, a_value_to_update)

        for idx, node in enumerate(state.team_std_info[self.data_kind]["children"]):
            if node["name"] == selected_qItem_name:
                state.team_std_info[self.data_kind]["children"].remove(node)
                state.team_std_info[self.data_kind]["children"].insert(idx, targetData)
                state.log_widget.write(str(targetData))

        # state.log_widget.write(str(targetData))
        return targetData

    def update(self, event=None, view_level=None):
        view_level = self.view_level
        self.state.log_widget.write(f"view_level {view_level}")
        state = self.state
        """Update the TreeView whenever the state changes."""
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        self.state.log_widget.write(
            f"관련위젯 선택항목 출력 : {self.selected_item_relate_widget.get()}"
        )

        try:
            # # Split the selected item path to find the grandparent, parent, and selected item names
            pattern = r"^\d+\.\d+$"
            selected_NoItem = go(
                self.selected_item_relate_widget.get().split(" | "),
                filter(lambda x: re.match(pattern, x)),
                next,
            )

            # selected_qItem_name = f"Q{selected_item_name}"
            selected_qItem_name = f"Q{selected_NoItem}"
            self.state.log_widget.write(f"산출유형번호 : {selected_qItem_name}")

            # Ensure the data kind exists in the team standard information
            if self.data_kind in state.team_std_info:
                data = state.team_std_info[self.data_kind]["children"]
                selected_node = next(
                    (node for node in data if node["name"] == selected_qItem_name),
                    None,
                )
                # print(selected_node)

                if selected_node:
                    # Clear the TreeView and insert the data for the selected node
                    self.treeview.clear_treeview()
                    self.treeview.insert_data_with_levels([selected_node])

                    # self.treeview.expand_tree_to_level(level=view_level)

        except Exception as e:
            self.state.log_widget.write(
                f"{self.__class__.__name__} > update 메소드 진입 안됩니다~: {e}"
            )

        # self.treeview.expand_all_items()
        self.treeview.expand_tree_to_level(level=view_level)
        # self.treeview.expand_tree_to_level(level=3)
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        # if self.last_selected_item:
        #     self.treeview.tree.item(self.treeview.last_selected_item, tags=("normal",))

        self.state.log_widget.write("on_item_selected_시작")
        selected_items_id = self.treeview.tree.selection()
        selected_items_name = go(
            selected_items_id,
            map(lambda x: list(self.treeview.tree.item(x, "values"))),
            list,
            map(lambda x: x[0]),
            list,
        )
        self.state.log_widget.write(str(selected_items_name))
        self.state.selected_matchedWMs = selected_items_name
        # # 마지막 선택항목으로 재등록
        # self.last_selected_item = selected_items_id[0]
        self.state.log_widget.write("on_item_selected_종료")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        self.state.log_widget.write(
            f"Parent IDs for selected item '{selected_item_id}': {parent_ids}"
        )
        return list(reversed(parent_ids))

    def add_top_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Top Item", "Enter the name of the new item:"
        )
        if new_item_name:
            self.treeDataManager.add_top_level_node(self.data_kind, new_item_name)
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def add_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Item", "Enter the name of the new item:"
        )
        if new_item_name:
            selected_item_id = self.treeview.tree.selection()
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )[0]
            self.treeDataManager.add_child_node(
                self.data_kind, selected_item_name, new_item_name
            )
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state

        selected_item_id = self.treeview.tree.selection()
        selected_item_name = go(
            selected_item_id,
            lambda x: self.treeview.tree.item(x, "values"),
            filter(lambda x: x != ""),
            list,
        )[0]

        self.treeDataManager.delete_node(
            self.data_kind,
            selected_item_name,
        )
        # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
        state.observer_manager.notify_observers(state)


class BuildingList_TreeView(ttk.Frame):
    def __init__(self, state, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True)
        self.state = state
        self.data_kind = "std-familylist"

        # Title Label
        ttk.Label(self, text="Building List", font=("Arial", 16)).pack(pady=10)

        headers = ["Building Name"]
        hdr_widths = [400]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        # self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        # self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

        # Input Field
        ttk.Label(self, text="Enter Building Name:", font=("Arial", 12)).pack(pady=5)
        self.entry = ttk.Entry(self, font=("Arial", 12), bootstyle=SECONDARY)
        self.entry.pack(pady=5, fill="x", padx=10)

        # Buttons for Add and Delete
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Add Building",
            command=self.add_building,
            bootstyle=SUCCESS,
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame,
            text="Delete Building",
            command=self.delete_building,
            bootstyle=DANGER,
        ).pack(side="left", padx=5)

        # Status Label
        self.status_label = ttk.Label(self, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def add_building(self):
        """Add a building name to the TreeView."""
        building_name = self.entry.get().strip()
        print(f"building_name: {building_name}")
        if building_name:
            self.treeview.tree.insert(
                "",
                "end",
                text=building_name,
                values=[building_name],
            )  # Add the building to the TreeView
            self.entry.delete(0, "end")  # Clear the entry field
            self.status_label.config(
                text=f"Building '{building_name}' added successfully.",
                bootstyle=SUCCESS,
            )
        else:
            self.status_label.config(
                text="Please enter a building name.", bootstyle=DANGER
            )
        print(self.treeview.tree.item(self.treeview.tree.get_children("")))

    def delete_building(self):
        """Delete the selected building from the TreeView."""
        selected_item = self.treeview.tree.selection()
        if selected_item:
            building_name = self.treeview.tree.item(selected_item, "text")
            self.treeview.tree.delete(selected_item)
            self.status_label.config(
                text=f"Building '{building_name}' deleted successfully.",
                bootstyle=SUCCESS,
            )
        else:
            self.status_label.config(
                text="Please select a building to delete.", bootstyle=DANGER
            )
