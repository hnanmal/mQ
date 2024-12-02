# src/views/widget/treeview_utils.py
from src.controllers.tree_data_navigator import TreeDataManager
from src.core.fp_utils import *
import tkinter as tk
from tkinter import (
    # ttk,
    simpledialog,
    messagebox,
)
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from src.views.widget.treeview_editor import TreeviewEditor


# Composition for Style Management
class DefaultTreeViewStyleManager:

    @staticmethod
    def apply_style(treeview):
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial Narrow", 10),
            highlightthickness=1,
            background="white",
            foreground="black",
            rowheight=30,
            height=50,
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

    def apply_locked_style(treeview):
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            font=("Arial Narrow", 10),
            highlightthickness=1,
            background="#fafafa",
            foreground="black",
            height=50,
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#fffec0")],  # Set the selection background color
            foreground=[("selected", "blue")],
        )  # Set the selection foreground color
        # Configure hover style
        style.configure(
            "Hover.Custom.Treeview", background="#d3d3d3", padding=(2, 2)
        )  # Light gray hover color
        style.configure("Custom.Treeview.Heading", font=("Arial Narrow", 10, "normal"))
        treeview.configure(style="Custom.Treeview")


# Composition for State Management
class TreeViewStateObserver:
    def __init__(self, state, updateFunc):
        self.state = state
        self.state.observer_manager.add_observer(lambda e: updateFunc(e))


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

        # Bind the right-click to show the menu
        self.treeview.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        # Debug statement to check locked status
        print(f"Context Menu Locked Status: {self.locked_status}")
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
        print(f"Locked Status Updated: {self.locked_status}")

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
    def __init__(self, parent, headers):
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

        # 이벤트 바인딩
        self.tree.bind(
            "<Motion>", self.on_mouse_motion
        )  # 마우스 움직임을 감지해 hover 효과 적용
        self.tree.bind(
            "<Leave>", self.on_mouse_leave
        )  # 트리뷰에서 마우스가 나갔을 때 hover 효과 제거

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

    def expand_all_items(self):
        """Recursively expand all items in the Treeview."""
        treeview = self.tree

        def expand_item(item):
            # Set the item to open (expanded)
            treeview.item(item, open=True)
            # Get the children of the current item
            children = treeview.get_children(item)
            for child in children:
                expand_item(child)

        # Get all root items
        root_items = treeview.get_children("")
        for item in root_items:
            expand_item(item)

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
                    node_id, open=True
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
                print(
                    f"Error: Item '{current_item}' not found among siblings {siblings}"
                )
                return []

            # Debug: print current processing details
            print(
                f"Current item: {current_item}, Parent ID: {parent_id}, Index: {item_index}"
            )

            # Insert the item index at the beginning of the list to maintain top-down order
            indices.insert(0, item_index)

            # Move to the parent item
            current_item = parent_id

        # Debug: print the final indices
        print(f"Final Indices: {indices}")
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
                print(f"Index {index} is out of bounds for the current parent.")
                return

        if target_item:
            self.tree.selection_set(target_item)
            self.tree.focus(target_item)
            self.tree.see(target_item)


class TeamStd_GWMTreeView:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "std-GWM"

        self.treeDataManager = TreeDataManager(state, self)
        self.state_observer = TreeViewStateObserver(state, self.update)

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "G-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(parent)
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
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(parent, text="Standard Types for GWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None):
        state = self.state
        print(f"{self.__class__.__name__} > update 메소드 시작")

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

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                print(f"Item selection failed: {e}")

        print(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        try:
            # Reset the tag for the previously selected item to 'normal'
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            print(f"Error resetting last selected item tag: {e}")

        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        self.treeview.last_selected_item = selected_item_id

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
            print(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        print(f"Parent IDs for selected item '{selected_item_id}': {parent_ids}")
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


class TeamStd_WMmatching_TreeView:
    def __init__(self, state, parent, relate_widget, data_kind=None):
        self.state = state
        self.data_kind = data_kind
        self.selected_item_relate_widget = relate_widget.selected_item
        headers = ["Work Master"]
        hdr_widths = [1000]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)
        self.state_observer = TreeViewStateObserver(state, self.update)

        # config selection mode
        self.treeview.tree.config(selectmode="extended")

        # Tag styles
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(parent)
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

    def update(self, event=None):
        state = self.state
        """Update the TreeView whenever the state changes."""
        print(f"{self.__class__.__name__} > update 메소드 시작")
        print(self.selected_item_relate_widget.get())

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
                            print(f"Selected item '{selected_item_name}' not found.")
                    else:
                        print(f"Parent item '{parent_item_name}' not found.")
                else:
                    print(f"Grandparent item '{grand_parent_item_name}' not found.")

        except Exception as e:
            print(f"{self.__class__.__name__} > update 메소드 진입 안됩니다~: {e}")

        print(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        # if self.last_selected_item:
        #     self.treeview.tree.item(self.treeview.last_selected_item, tags=("normal",))

        print("on_item_selected_시작")
        selected_items_id = self.treeview.tree.selection()
        selected_items_name = go(
            selected_items_id,
            map(lambda x: list(self.treeview.tree.item(x, "values"))),
            list,
            map(lambda x: x[0]),
            list,
        )
        print(selected_items_name)
        self.state.selected_matchedWMs = selected_items_name
        # # 마지막 선택항목으로 재등록
        # self.last_selected_item = selected_items_id[0]
        print("on_item_selected_종료")


class TeamStd_SWMTreeView:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "std-SWM"

        self.treeDataManager = TreeDataManager(state, self)
        self.state_observer = TreeViewStateObserver(state, self.update)

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "S-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(parent)
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
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(parent, text="Standard Types for SWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None):
        state = self.state
        print(f"{self.__class__.__name__} > update 메소드 시작")

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

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                print(f"Item selection failed: {e}")

        print(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        try:
            # Reset the tag for the previously selected item to 'normal'
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            print(f"Error resetting last selected item tag: {e}")

        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        self.treeview.last_selected_item = selected_item_id

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
            print(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        print(f"Parent IDs for selected item '{selected_item_id}': {parent_ids}")
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


###################for common_input################################################################


class TeamStd_CommonInputTreeView:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "common-input"

        self.treeDataManager = TreeDataManager(state, self)
        self.state_observer = TreeViewStateObserver(state, self.update)

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "Abbreviation", "Description", "Input", "Unit", "Remark"]
        hdr_widths = [127, 125, 200, 50, 50, 200]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(parent)
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

    def update(self, event=None):
        state = self.state
        print(f"{self.__class__.__name__} > update 메소드 시작")

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

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                print(f"Item selection failed: {e}")

        print(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        try:
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            print(f"Error resetting last selected item tag: {e}")

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
            print(f"IndexError: {e}")
        except Exception as e:
            print(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        print(f"Parent IDs for selected item '{selected_item_id}': {parent_ids}")
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


################################


class TeamStd_FamlistTreeView:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "std-familylist"

        self.treeDataManager = TreeDataManager(state, self)
        self.state_observer = TreeViewStateObserver(state, self.update)

        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = [
            "분류",
            "No",
            "Family Name",
            "Description",
            "G-WM 1",
            "G-WM 2",
            "G-WM 3",
            "G-WM 4",
            "S-WM 1",
            "표준물량 산출식",
        ]
        hdr_widths = [60, 10, 100, 200, 30, 30, 30, 30, 30, 30]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        # self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial Narrow", 10))
        # Set up UI
        self.set_title(parent)
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
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def set_title(self, parent):
        title_font = ttk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(parent, text="Standard Family List", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def update(self, event=None):
        state = self.state
        print(f"{self.__class__.__name__} > update 메소드 시작")

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

        # Reselect the item if possible
        if origin_indices:
            try:
                self.treeview.select_item_by_indices(origin_indices)
            except Exception as e:
                print(f"Item selection failed: {e}")

        print(f"{self.__class__.__name__} > update 메소드 종료")

    def on_item_selected(self, event):
        try:
            # Reset the tag for the previously selected item to 'normal'
            if self.last_selected_item:
                self.treeview.tree.item(self.last_selected_item, tags=("normal",))
        except Exception as e:
            print(f"Error resetting last selected item tag: {e}")

        # Get the currently selected item
        selected_item_id = self.treeview.tree.focus()
        self.treeview.last_selected_item = selected_item_id

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
            print(f"Error processing selected item details: {e}")

    def get_parent_ids(self, selected_item_id):
        parent_ids = []
        current_item = selected_item_id

        while current_item:
            parent_id = self.treeview.tree.parent(current_item)
            if parent_id:  # 부모 항목이 있을 경우에만 리스트에 추가
                parent_ids.append(parent_id)
            current_item = parent_id

        # Debug: print the final list of parent IDs
        print(f"Parent IDs for selected item '{selected_item_id}': {parent_ids}")
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
