# src/views/widget/treeview_utils.py
from src.core.fp_utils import *
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


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
    def __init__(self, state, treeview, data_kind=None):
        self.state = state
        self.treeview = treeview
        self.locked_status = None
        self.data_kind = data_kind
        # Create the context menu
        self.menu = tk.Menu(self.treeview.tree, tearoff=0)
        self.menu.add_command(label="Add Item", command=self.add_item)
        self.menu.add_command(label="Edit Item", command=self.edit_item)
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

    def add_item(self):
        state = self.state
        # Prompt the user for the new item name
        new_item_name = simpledialog.askstring(
            "Add Item", "Enter the name of the new item:"
        )
        selected_item_id = self.treeview.tree.selection()
        selected_item_name = go(
            selected_item_id,
            lambda x: self.treeview.tree.item(x, "values"),
            filter(lambda x: x != ""),
            list,
        )
        parents = self.get_parent_ids(selected_item_id)
        print(parents)
        parents_names = go(
            parents,
            map(lambda x: self.treeview.tree.item(x, "values")),
            lambda x: chain(*x),
            filter(lambda x: x != ""),
            list,
        )

        if len(parents) == 0:
            [lv1_key] = selected_item_name
            self.state.team_std_info[self.data_kind][lv1_key].update(
                {new_item_name: {}}
            )
        elif len(parents) == 1:
            [lv1_key] = parents_names
            [lv2_key] = selected_item_name
            self.state.team_std_info[self.data_kind][lv1_key][lv2_key].update(
                {new_item_name: []}
            )
        # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
        state.observer_manager.notify_observers(state)

    def edit_item(self):
        state = self.state
        selected_item_id = self.treeview.tree.selection()
        if selected_item_id:
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )
            parents = self.get_parent_ids(selected_item_id)
            print(parents)
            parents_names = go(
                parents,
                map(lambda x: self.treeview.tree.item(x, "values")),
                lambda x: chain(*x),
                filter(lambda x: x != ""),
                list,
            )
            current_value = selected_item_name

            new_value = simpledialog.askstring(
                "Edit Item", "Edit the item:", initialvalue=current_value
            )
            if new_value:
                # Update the item with the new value
                if len(parents) == 0:
                    [lv1_key] = selected_item_name
                    v = self.state.team_std_info[self.data_kind].pop(lv1_key)
                    self.state.team_std_info[self.data_kind].update({new_value: v})
                elif len(parents) == 1:
                    [lv1_key] = parents_names
                    [lv2_key] = selected_item_name
                    v = self.state.team_std_info[self.data_kind][lv1_key].pop(lv2_key)
                    self.state.team_std_info[self.data_kind][lv1_key].update(
                        {new_value: v}
                    )
                elif len(parents) == 2:
                    [lv1_key, lv2_key] = parents_names
                    [lv3_key] = selected_item_name
                    v = self.state.team_std_info[self.data_kind][lv1_key][lv2_key].pop(
                        lv3_key
                    )
                    self.state.team_std_info[self.data_kind][lv1_key][lv2_key].update(
                        {new_value: v}
                    )
        else:
            messagebox.showwarning("No Selection", "Please select an item to edit.")

        # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
        state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state
        selected_item_id = self.treeview.tree.selection()
        if selected_item_id:
            selected_item_name = go(
                selected_item_id,
                lambda x: self.treeview.tree.item(x, "values"),
                filter(lambda x: x != ""),
                list,
            )
            parents = self.get_parent_ids(selected_item_id)
            print(parents)
            parents_names = go(
                parents,
                map(lambda x: self.treeview.tree.item(x, "values")),
                lambda x: chain(*x),
                filter(lambda x: x != ""),
                list,
            )
            confirm = messagebox.askyesno(
                "Delete Item", "Are you sure you want to delete the selected item?"
            )
            if confirm:
                # Delete the selected item
                if len(parents) == 0:
                    [lv1_key] = selected_item_name
                    v = self.state.team_std_info[self.data_kind].pop(lv1_key)
                elif len(parents) == 1:
                    [lv1_key] = parents_names
                    [lv2_key] = selected_item_name
                    v = self.state.team_std_info[self.data_kind][lv1_key].pop(lv2_key)
                elif len(parents) == 2:
                    [lv1_key, lv2_key] = parents_names
                    [lv3_key] = selected_item_name
                    v = self.state.team_std_info[self.data_kind][lv1_key][lv2_key].pop(
                        lv3_key
                    )
        else:
            messagebox.showwarning("No Selection", "Please select an item to delete.")

        # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
        state.observer_manager.notify_observers(state)


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
        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "G-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)

        self.state_observer = TreeViewStateObserver(state, self.update)

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

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Create and integrate context menu
        self.context_menu = TreeViewContextMenu(
            state, self.treeview, data_kind=self.data_kind
        )
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def update(self, event=None):
        state = self.state
        print("TeamStd_GWMTreeView > update 메소드 시작")

        selected_item_id = self.treeview.tree.focus()
        try:
            origin_indices = self.treeview.get_item_indices(selected_item_id)
            print(origin_indices, "!!!")
        except:
            print("origin_indices 추출 실패")

        """Update the TreeView whenever the state changes."""
        if "std-GWM" in state.team_std_info:
            # Clear the TreeView and reload data from the updated state
            data = state.team_std_info[self.data_kind]
            # treeview_data = self.treeview.get_tree_data()
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

        try:
            self.treeview.select_item_by_indices(origin_indices)
        except:
            pass
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

            # self.state.selected_stdGWM_item.set(formatted_value)
            self.selected_item.set(formatted_value)


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

        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    # def update(self, state):
    def update(self, event=None):
        state = self.state
        """Update the TreeView whenever the state changes."""
        print("TeamStd_GWMmatching_TreeView > update 메소드 시작")
        print(self.selected_item_relate_widget.get())
        try:
            self.selected_item_relate_widget.get().split(" | ")

            grand_parent_item_name, parent_item_name, selected_item_name = (
                self.selected_item_relate_widget.get().split(" | ")
            )
            if self.data_kind in self.state.team_std_info:
                self.treeview.clear_treeview()
                data = self.state.team_std_info[self.data_kind][grand_parent_item_name][
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
        title_label = tk.Label(
            parent, text="Matched WMs for Selected Standard Types", font=title_font
        )
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
        # print(selected_items_name)
        print("on_item_selected_종료")


class TeamStd_SWMTreeView:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "std-SWM"
        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)
        headers = ["분류", "S-WM", "Item"]
        hdr_widths = [127, 60, 100]

        # Compose TreeView, Style Manager, and State Observer
        tree_frame = ttk.Frame(parent, width=600, height=2000)
        self.treeview = BaseTreeView(tree_frame, headers)
        self.treeview.tree.config(height=3000)

        self.state_observer = TreeViewStateObserver(state, self.update)

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

        # Track the last selected item with an instance attribute
        self.last_selected_item = None
        # Bind selection events
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Create and integrate context menu
        self.context_menu = TreeViewContextMenu(state, self.treeview, self.data_kind)
        # state.edit_mode_manager.register_widgets(treeCtxtMenu=[self.context_menu])

    def update(self, event=None):
        state = self.state
        print("TeamStd_GWMTreeView > update 메소드 시작")

        selected_item_id = self.treeview.tree.focus()
        try:
            origin_indices = self.treeview.get_item_indices(selected_item_id)
            print(origin_indices, "!!!")
        except:
            print("origin_indices 추출 실패")

        """Update the TreeView whenever the state changes."""
        if "std-SWM" in state.team_std_info:
            # Clear the TreeView and reload data from the updated state
            data = state.team_std_info[self.data_kind]
            # treeview_data = self.treeview.get_tree_data()
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

        try:
            self.treeview.select_item_by_indices(origin_indices)
        except:
            pass
        print("TeamStd_GWMTreeView > update 메소드 종료")

    def set_title(self, parent):
        title_font = tk.font.Font(family="맑은 고딕", size=12)
        title_label = tk.Label(parent, text="Standard Types for SWM", font=title_font)
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

            self.selected_item.set(formatted_value)
