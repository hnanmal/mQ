import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.controllers.tree_data_navigator import TreeDataManager_treeview
from src.core.fp_utils import *
from src.views.widget.widget import StateObserver, open_dialog
from src.views.widget.multiline_input import MultiLineInputFrame
from src.views.widget.treeview_utils import BaseTreeView, ScrollbarWidget
from src.views.widget.treeview_editor import TreeviewEditor


## Revit Type 입력시 편의를 위해 rvt summary 시트 더블클릭 새창 열기 기능 구현 필수
## 여러 레빗타입을 동시에 같은 내용으로 편집하게 하려면 구성을 어떻게 하는게 좋을지?
## >> 그룹 지정 / 해제 기능을 만들면 편할듯?
## >> 아니면, 레빗 타입 다중 선택 상태에서 우측 내용 입력후 확정 버튼을 누르면 동시에 데이터 주입되도록?
## >> 확정후에 레벳 타입 하나씩 누르면 각각에 대한 상태 우측에 표시하고,
## >> 여러개 눌러서 보면 동일하면 그 상태 보여주고, 다른 종류가 섞여있으면 var 로 표시하게 하던지?
## >> 아니면 스타일 복사 버튼?
## >> 다중선택 이랑 스타일 복사 두개 다 있어야 할거 같다


class TypeAssign_treeview:  ## delete 함수 수정 & 항목 클릭시 state에 선택항목 반영하도록 수정필요
    def __init__(self, state, parent, relate_widget, view_level=2, *args, **kwargs):
        self.state = state
        # self.data_kind = "project-buildinglist"
        self.data_kind = "project-assigntype"
        self.relate_widget = relate_widget
        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.state_observer = StateObserver(state, lambda e: self.update(e))
        self.selected_item = tk.StringVar()
        self.selected_item.trace_add("write", state._notify_selected_change)

        self.frame = ttk.Frame(parent)
        self.frame.pack(padx=10, side="top", anchor="nw")

        ## attach, detach 버튼 구간
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(anchor="center")

        self.attach_button = ttk.Button(
            button_frame,
            # text="Attach\nto the Std Type",
            text="⬇",
            command=self.add_item,
            bootstyle="outline",
        )
        self.attach_button.pack(padx=10, anchor="center", side="left")

        self.detach_button = ttk.Button(
            button_frame,
            # text="Detach\nfrom the Std Type",
            text="⬆",
            bootstyle="warning-outline",
        )
        self.detach_button.pack(padx=10, anchor="center", side="left")

        # Compose TreeView, Style Manager, and State Observer
        # headers = ["Top", "Revit Type"]
        # hdr_widths = [0, 350]
        headers = ["Revit Type", "Building", "Std Type"]
        hdr_widths = [200, 100, 100]
        tree_frame = ttk.Frame(self.frame, width=350, height=3000)
        tree_frame.pack(padx=10, pady=10, side="top", fill="both")
        self.tree_frame = tree_frame
        self.treeview = BaseTreeView(state, tree_frame, headers)

        # config selection mode
        self.treeview.tree.config(selectmode="extended")
        self.treeview.tree.column(0, width=0, minwidth=0, stretch=False)
        # self.set_title(tree_frame)
        self.scroll_widget = ScrollbarWidget(tree_frame, self.treeview.tree)
        self.treeview.tree.pack(expand=True, fill="both", side="top", anchor="nw")
        self.treeview.setup_columns(headers, hdr_widths)

        # set treeview_editor class
        self.treeviewEditor = TreeviewEditor(state, self)

    def update(self, event=None, view_level=None):
        state = self.state
        state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        selected_stdType = self.relate_widget.selected_item_relate_widget.get()

        """Update the TreeView whenever the state changes."""
        if self.data_kind in state.team_std_info:
            # data = state.team_std_info[self.data_kind]["children"]
            data = go(
                state.team_std_info.get(self.data_kind).get("children"),
                filter(lambda x: x["values"][1] == state.current_building.get()),
                filter(lambda x: x["values"][-1] == selected_stdType),
                list,
                # lambda x: x[0],
            )

            # Clear the TreeView and reload data from the updated state
            self.treeview.clear_treeview()
            self.treeview.insert_data_with_levels(data)

            self.treeview.expand_tree_to_level(level=view_level)

        state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def add_item(self):
        """Add a building name to the TreeView."""
        state = self.state
        current_building = state.current_building.get()
        selected_stdType = self.relate_widget.selected_item_relate_widget.get()

        if current_building == "건물을 선택하세요":
            open_dialog(
                state.root,
                "건물을 선택하셔야 합니다.",
            )
            return
        if not selected_stdType:
            open_dialog(
                state.root,
                "좌측 표준타입을 선택하셔야 합니다.",
            )
            return

        data = go(
            state.team_std_info.get(self.data_kind),
            # filter(lambda x: x["name"] == state.current_building.get()),
            # list,
            # lambda x: x[0],
        )
        item_names = self.relate_widget.entry.get_text().split("\n")

        def _add(item_name):
            # item_name = self.relate_widget.entry.get().strip()
            state.log_widget.write(f"타입: {item_name}")
            if item_name:
                # self.treeDataManager.add_top_level_node(self.data_kind, item_name)
                data["children"].append(
                    {
                        "name": item_name,
                        # "values": ["", item_name],
                        "values": [
                            item_name,
                            current_building,
                            selected_stdType,
                        ],
                        "children": [],
                    }
                )
                self.relate_widget.entry.clear_text()  # Clear the entry field

                # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
                state.observer_manager.notify_observers(state)
            else:
                state.log_widget.write("Please enter a revit type name.")

        for item_name in item_names:
            _add(item_name)


class ModelType_entry:
    def __init__(self, state, parent, relate_widget):
        self.state = state
        self.data_kind = "project-buildinglist"
        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.relate_widget = relate_widget
        self.selected_item_relate_widget = relate_widget.selected_item
        # self.state_observer = StateObserver(state, lambda e: self.update(e))

        self.frame = ttk.Frame(parent)
        self.frame.pack(padx=10, side="top", anchor="nw")

        label_frame = ttk.Frame(self.frame)
        label_frame.pack(anchor="nw")

        widget_frame = ttk.Frame(self.frame)
        widget_frame.pack(anchor="nw")

        self.create_assign_label(label_frame)

        self.create_rvtType_entry(widget_frame)
        self.entry = self.rvtType_entry

    def create_assign_label(self, frame):
        label_static = ttk.Label(frame, text="Assigned for :")
        label_static.config(font=("Arial", 12, "normal"))
        label_static.pack(padx=2, side="left", anchor="w")

        label_dynamic = ttk.Label(frame, textvariable=self.selected_item_relate_widget)
        label_dynamic.config(font=("Arial", 12, "normal"), foreground="blue")
        label_dynamic.pack(padx=2, side="left", anchor="w")

    def create_rvtType_entry(self, frame):
        state = self.state
        self.rvtType_entry = MultiLineInputFrame(
            state,
            frame,
            label_text="Enter Revit Type",
        )
        self.rvtType_entry.text_widget.config(height=3)  # Change to 15 rows
        self.rvtType_entry.pack(fill="x", expand=True, padx=10, pady=10)
