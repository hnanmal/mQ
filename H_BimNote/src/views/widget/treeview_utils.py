# src/views/widget/treeview_utils.py
from src.core.fp_utils import *
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
        # Configure hover style
        style.configure(
            "Hover.Treeview", background="#d3d3d3", padding=(2, 2)
        )  # Light gray hover color
        style.configure("Treeview.Heading", font=("Arial", 10, "normal"))
        treeview.configure(style="Treeview")


# Composition for State Management
class TreeViewStateObserver:
    def __init__(self, state, treeview, updateFunc):
        self.state = state
        self.state.observer_manager.add_observer(updateFunc)


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


class BaseTreeView:
    def __init__(self, parent, headers):
        self.tree = ttk.Treeview(parent, columns=headers, show="headings")
        self.setup_columns(headers)
        self.parent = parent
        # Configure tag styles
        self.tree.tag_configure(
            "hover",
            background="#d3d3d3",
            foreground="blue",
            font=("Arial", 10, "bold"),
            # padding=(2, 2),
        )  # Light gray background for hover
        self.tree.tag_configure(
            "normal", background="white"
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
                pass
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

    def get_item_indices(self, selected_item_id):
        """
        Get the list of indices from the highest-level parent down to the selected item.

        Parameters:
        tree (ttk.Treeview): The Treeview widget.
        selected_item_id (str): The ID of the selected item.

        Returns:
        list: A list of indices representing the path from the highest-level parent to the selected item.
        """
        indices = []

        current_item = selected_item_id
        while current_item:
            # Get the parent of the current item
            parent_id = self.tree.parent(current_item)

            # Get all the siblings of the current item (including the current item itself)
            siblings = self.tree.get_children(parent_id)

            # Find the index of the current item among its siblings
            position = siblings.index(current_item)

            # Insert the position at the beginning of the list (to maintain top-down order)
            indices.insert(0, position)

            # Move up one level to the parent
            current_item = parent_id

        return indices

    def select_item_by_indices(self, indices):
        """
        Select an item in the Treeview using the provided list of indices.

        Parameters:
        tree (ttk.Treeview): The Treeview widget.
        indices (list): A list of indices representing the path from the highest-level parent to the desired item.
        """
        current_parent = ""  # Start from the root
        target_item = None

        for index in indices:
            # Get all children of the current parent
            children = self.tree.get_children(current_parent)

            # Make sure the index is within bounds
            if index < len(children):
                target_item = children[index]
                current_parent = target_item
            else:
                # If the index is out of bounds, it means something went wrong
                print(f"Index {index} is out of bounds for the current parent.")
                return

        # If a target item was found, select it
        if target_item:
            self.tree.selection_set(target_item)
            self.tree.focus(target_item)
            self.tree.see(target_item)  # Scroll to the selected item if needed
            self.last_selected_item = target_item


class TeamStd_GWMTreeView:
    def __init__(self, state, parent):
        self.state = state
        headers = ["분류", "G-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)
        self.state_observer = TreeViewStateObserver(
            state, self.treeview, lambda e: self.update(state)
        )

        # config selection mode
        self.treeview.tree.config(selectmode="browse")
        # Tag styles
        self.treeview.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.treeview.tree.tag_configure("normal", font=("Arial", 10))
        # Set up UI
        self.set_title(parent)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def update(self, state):
        selected_item_id = self.treeview.tree.selection()
        origin_indices = self.treeview.get_item_indices(selected_item_id)

        print("TeamStd_GWMTreeView > update 메소드 시작")
        """Update the TreeView whenever the state changes."""
        if "std-GWM" in state.team_std_info:
            # Clear the TreeView and reload data from the updated state
            self.treeview.clear_treeview()
            data = state.team_std_info["std-GWM"]
            self.treeview.insert_data_with_levels(data)

        self.treeview.select_item_by_indices(origin_indices)
        print("TeamStd_GWMTreeView > update 메소드 종료")

    def set_title(self, parent):
        title_font = tk.font.Font(family="맑은 고딕", size=12)
        title_label = tk.Label(parent, text="Standard Types for GWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def on_item_selected(self, event):
        if self.last_selected_item:
            self.treeview.tree.item(self.treeview.last_selected_item, tags=("normal",))

        # selected_item_id = self.treeview.tree.selection()
        selected_item_id = self.treeview.tree.focus()
        self.treeview.last_selected_item = selected_item_id
        parent_item_id = self.treeview.tree.parent(selected_item_id)
        grand_parent_item_id = self.treeview.tree.parent(parent_item_id)

        if self.treeview.tree.item(selected_item_id, "values")[-1]:
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


class TeamStd_GWMmatching_TreeView:
    def __init__(self, state, parent):
        self.state = state
        headers = ["Work Master"]
        hdr_widths = [1000]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)
        self.state_observer = TreeViewStateObserver(
            state, self.treeview, lambda e: self.update(state)
        )

        # config selection mode
        self.treeview.tree.config(selectmode="extended")

        # Set up UI
        self.set_title(parent)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="left")
        self.treeview.setup_columns(headers, hdr_widths)

        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    # def update(self, state):
    def update(self, state):
        """Update the TreeView whenever the state changes."""
        print("TeamStd_GWMmatching_TreeView > update 메소드 시작")
        print(state.selected_stdGWM_item.get())
        try:
            self.state.selected_stdGWM_item.get().split(" | ")

            grand_parent_item_name, parent_item_name, selected_item_name = (
                self.state.selected_stdGWM_item.get().split(" | ")
            )
            if "std-GWM" in self.state.team_std_info:
                self.treeview.clear_treeview()
                data = self.state.team_std_info["std-GWM"][grand_parent_item_name][
                    parent_item_name
                ][selected_item_name]
                wrapped_data = list(map(lambda x: [x], data))
                self.treeview.insert_data(wrapped_data)
        except:
            print("TeamStd_GWMmatching_TreeView > update 메소드 진입 안됩니다~")
            pass
        print("TeamStd_GWMmatching_TreeView > update 메소드 종료")

    def set_title(self, parent):
        title_font = tk.font.Font(family="맑은 고딕", size=12)
        title_label = tk.Label(parent, text="Standard Types for GWM", font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def on_item_selected(self, event):
        print("on_item_selected_시작")
        selected_items_id = self.treeview.tree.selection()
        selected_items_name = go(
            selected_items_id,
            map(lambda x: list(self.treeview.tree.item(x, "values"))),
            list,
            map(lambda x: x[0]),
            list,
        )
        self.state.selected_matchedWMs = selected_items_name
        print(selected_items_name)
        print("on_item_selected_종료")
