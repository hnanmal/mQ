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


class WMapply_button:
    def __init__(self, state, parent, ref_widgets, tgt_widget, *args, **kwargs):
        self.state = state
        self.data_kind = self.data_kind = "project-assigntype-WM"

        self.ref_widgets = ref_widgets
        self.familylist_widget = ref_widgets[0]
        self.GWMwidget = ref_widgets[1]
        self.SWMwidget = ref_widgets[2]
        self.typeAssign_treeview = ref_widgets[3]

        self.tgt_widget = tgt_widget

        ## set ui
        self.set_ui(parent)

    def set_ui(self, parent):
        state = self.state
        button_frame = ttk.Frame(
            parent,
            # relief="ridge",
            # borderwidth=3,
        )
        button_frame.pack(
            expand=True,
            fill="x",
            # padx=430,
            padx=10,
            pady=10,
            side="bottom",
            anchor="center",
        )

        attach_button = ttk.Button(
            button_frame,
            text="⬇     산출항목 결정하기     ⬇",
            width=100,
            command=self.match_WM_to_rvtType,
            # bootstyle="outline",
            bootstyle="info-outline",
        )
        attach_button.pack(
            # expand=True,
            padx=30,
            anchor="center",
            # side="left",
        )

        return button_frame

    def get_checked_GWMSWM(self, GWMwidget, SWMwidget):
        state = self.state

        pjt_gwm_data = state.team_std_info.get("project-GWM")
        pjt_swm_data = state.team_std_info.get("project-SWM")
        WMs = state.team_std_info.get("WMs")

        WMsStr = go(
            WMs,
            map(lambda x: list(map(str, x))),
            map(lambda x: filter(lambda x: x != "0", x)),
            map(lambda x: filter(lambda x: x != "", x)),
            map(lambda x: filter(lambda x: x != " ", x)),
            map(lambda x: filter(lambda x: x != "ㅤ", x)),  #  공백 특수 문자
            map(lambda x: " | ".join(x)),
            list,
        )

        current_building = state.current_building.get()
        selected_stdType = self.familylist_widget.selected_item.get()
        selected_rvtTypes_ids = self.typeAssign_treeview.treeview.tree.selection()
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
        if not selected_rvtTypes_ids:
            open_dialog(
                state.root,
                "중앙의 레빗타입을 선택하셔야 합니다.",
            )
            return

        # std_type_no = self.familylist_widget.selected_item.split(" | ")[-1]
        std_type_no = go(
            self.familylist_widget.tree,
            lambda x: x.selection()[0],
            lambda x: self.familylist_widget.tree.item(x, "values"),
            lambda x: x[2],  ## type name 위치
        )
        std_type_name = go(
            self.familylist_widget.tree,
            lambda x: x.selection()[0],
            lambda x: self.familylist_widget.tree.item(x, "values"),
            lambda x: x[3],  ## type name 위치
        )
        # print(f"std_type_name :: {std_type_name}")

        chked_GWM_obj = GWMwidget.get_checked()
        chked_GWM_all = GWMwidget.sheet.get_sheet_data()
        chked_SWM_obj = SWMwidget.get_checked()

        def find_matched_pjtGWM(name):
            res = go(
                pjt_gwm_data.keys(),
                list,
                filter(lambda x: name in x),
                list,
            )
            try:
                return res[0]
            except:
                return ""

        def find_matched_pjtSWM(name):
            res = go(
                pjt_swm_data.keys(),
                list,
                filter(lambda x: name in x),
                list,
            )
            try:
                return res[0]
            except:
                return ""

        def find_wmStr(wmcode):
            res = go(
                WMsStr,
                filter(lambda x: wmcode in x),
                list,
            )
            try:
                return res[0]
            except:
                return ""

        if chked_GWM_obj:
            ref_keys = go(
                chked_GWM_obj.keys(),
                list,
                filter(lambda x: GWMwidget.sheet.get_cell_data(r=x[0], c=x[1])),
                map(lambda x: GWMwidget.sheet.get_cell_data(r=x[0], c=x[1] + 1)),
                list,
            )
            eff_chked_GWM = go(
                chked_GWM_all,
                filter(lambda x: x[0] != True),
                filter(lambda x: x[2] in ref_keys),
                list,
            )

            # print(ref_keys)
            chked_GWM = go(
                eff_chked_GWM,
                map(
                    lambda x: [
                        "GWM",
                        std_type_name,
                        " | ".join([x[2], x[3]]),
                        pjt_gwm_data.get(
                            find_matched_pjtGWM(" | ".join([x[2], x[3]])), ["", "", ""]
                        )[0],
                        pjt_gwm_data.get(
                            find_matched_pjtGWM(" | ".join([x[2], x[3]])), ["", "", ""]
                        )[1],
                        pjt_gwm_data.get(
                            find_matched_pjtGWM(" | ".join([x[2], x[3]])), ["", "", ""]
                        )[3],
                        x[-1],
                        pjt_gwm_data.get(
                            find_matched_pjtGWM(" | ".join([x[2], x[3]])), ["", "", ""]
                        )[2],
                        x[-2],
                    ]
                ),
                list,
            )

            chked_GWM_data = []
            for i in chked_GWM:
                x = deepcopy(i)
                # print(i[3])
                x[3] = find_wmStr(i[3])
                chked_GWM_data.append(x)

        else:
            chked_GWM_data = []

        if chked_SWM_obj:
            filtered_chked_SWM = go(
                chked_SWM_obj.keys(),
                list,
                filter(lambda x: SWMwidget.sheet.get_cell_data(r=x[0], c=x[1])),
                list,
            )
            chked_SWM_lv1 = go(
                filtered_chked_SWM,
                map(lambda x: [x[0], x[1] + 2]),
                list,
                map(lambda x: SWMwidget.sheet.get_cell_data(r=x[0], c=x[1])),
                list,
            )
            chked_SWM_lv2 = go(
                filtered_chked_SWM,
                map(lambda x: [x[0], x[1] + 3]),
                list,
                map(lambda x: SWMwidget.sheet.get_cell_data(r=x[0], c=x[1])),
                list,
            )
            chked_SWM_formula = go(
                filtered_chked_SWM,
                map(lambda x: [x[0], x[1] + 5]),
                list,
                map(lambda x: SWMwidget.sheet.get_cell_data(r=x[0], c=x[1])),
                list,
            )
            chked_SWM_calcNo = go(
                filtered_chked_SWM,
                map(lambda x: [x[0], x[1] + 4]),
                list,
                map(lambda x: SWMwidget.sheet.get_cell_data(r=x[0], c=x[1])),
                list,
            )
            chked_SWM = go(
                zip(
                    chked_SWM_lv1,
                    chked_SWM_lv2,
                    chked_SWM_calcNo,
                    chked_SWM_formula,
                ),
                map(
                    lambda x: [
                        "SWM",
                        std_type_name,
                        " | ".join([x[0], x[1]]),
                        pjt_swm_data.get(
                            find_matched_pjtSWM(" | ".join([x[0], x[1]])), ["", "", ""]
                        )[0],
                        pjt_swm_data.get(
                            find_matched_pjtSWM(" | ".join([x[0], x[1]])), ["", "", ""]
                        )[1],
                        pjt_swm_data.get(
                            find_matched_pjtSWM(" | ".join([x[0], x[1]])), ["", "", ""]
                        )[3],
                        x[-1],
                        pjt_swm_data.get(
                            find_matched_pjtSWM(" | ".join([x[0], x[1]])), ["", "", ""]
                        )[2],
                        x[-2],
                    ]
                ),
                list,
            )

            chked_SWM_data = []
            for i in chked_SWM:
                x = deepcopy(i)
                # print(i[3])
                x[3] = find_wmStr(i[3])
                chked_SWM_data.append(x)
        else:
            chked_SWM_data = []

        res = {
            "chked_GWM": chked_GWM_data,
            "chked_SWM": chked_SWM_data,
        }

        state.log_widget.write(str(res))

        return res

    def match_WM_to_rvtType(
        self,
    ):
        state = self.state

        data = state.team_std_info.get("project-assigntype")
        gwm_data = self.get_checked_GWMSWM(self.GWMwidget, self.SWMwidget)["chked_GWM"]
        swm_data = self.get_checked_GWMSWM(self.GWMwidget, self.SWMwidget)["chked_SWM"]

        selected_rvtTypes_ids = self.typeAssign_treeview.treeview.tree.selection()
        selected_rvtTypes_values = go(
            selected_rvtTypes_ids,
            map(lambda x: self.typeAssign_treeview.treeview.tree.item(x, "values")),
            list,
        )

        match_assigntype = lambda selected_rvtTypes_value: go(
            data["children"],
            filter(lambda x: x["values"][0] == selected_rvtTypes_value[0]),
            filter(lambda x: x["values"][1] == selected_rvtTypes_value[1]),
            filter(lambda x: x["values"][2] == selected_rvtTypes_value[2]),
            list,
            lambda x: x[0],
        )

        # Get the full path of the selected item
        for selected_rvtTypes_value in selected_rvtTypes_values:
            matched_assigntype = match_assigntype(selected_rvtTypes_value)
            total_WM_data = gwm_data + swm_data
            matched_assigntype["children"].extend(total_WM_data)

            print(f"selected_rvtTypes_value: {selected_rvtTypes_value}")
            print(f"matched_assigntype: {matched_assigntype['children']}")
            print(f"total_WM_data: {total_WM_data}")

        ## project_WM_perRVT_SheetView 업데이트
        state.project_WM_perRVT_SheetView.update()


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
            command=self.delete_item,
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

        # Bind selection events
        self.treeview.tree.bind(
            "<<TreeviewSelect>>", lambda e: self.on_item_selected(e)
        )

    def on_item_selected(self, event):
        state = self.state
        selected_item_ids = self.treeview.tree.selection()
        # selected_item_ids_str = ",".join(selected_item_ids)
        selected_item_names = go(
            selected_item_ids,
            map(lambda x: self.treeview.tree.item(x, "text")),
            list,
        )
        selected_item_names_str = ",,".join(selected_item_names)
        state.selected_rvtTypes.set(selected_item_names_str)

        # if len(selected_item_names) == 1:
        #     selected_item_names_str_forLabel = f"선택 : [ {selected_item_names[0]} ]"
        # else:
        #     selected_item_names_str_forLabel = f"선택 : [ {selected_item_names[0]} ] 외 {len(selected_item_names)-1} 개 항목"

        # state.selected_rvtTypes_forLabel.set(selected_item_names_str_forLabel)

        try:
            if len(selected_item_names) == 1:
                selected_item_names_str_forLabel = (
                    f"선택 : [ {selected_item_names[0]} ]"
                )
            else:
                selected_item_names_str_forLabel = f"선택 : [ {selected_item_names[0]} ] 외 {len(selected_item_names)-1} 개 항목"

            state.selected_rvtTypes_forLabel.set(selected_item_names_str_forLabel)
        except:
            pass

        ## project_WM_perRVT_SheetView 업데이트
        state.project_WM_perRVT_SheetView.update()

        state.log_widget.write(
            f"\n 선택된 레빗 타입 : {'  ,  '.join(selected_item_names)}\n"
        )

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
        elif not selected_stdType:
            self.treeview.clear_treeview()

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

            else:
                state.log_widget.write("Please enter a revit type name.")

        for item_name in item_names:
            _add(item_name)

        # print(f"\n item_names  ::  {item_names}\n")
        if item_names != [""]:
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            state.observer_manager.notify_observers(state)

    def delete_item(self):
        state = self.state

        # Get the selected item ID
        selected_item_ids = self.treeview.tree.selection()
        if not selected_item_ids:
            print("No item selected.")
            return
        # selected_item_id = selected_item_id[0]  # Handle single selection case

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

        return_str = []
        for selected_item_id in selected_item_ids:
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

            return_str.append(self.treeview.tree.item(selected_item_id, "text"))

        self.relate_widget.entry.set_text("\n".join(return_str))

        # Notify observers about the state update
        state.observer_manager.notify_observers(state)


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
