# src/models/app_state.py
from src.controllers.tree_data_navigator import TreeDataManager_treeview
from src.controllers.widget.widgets import EditModeManager
from src.core.fp_utils import *
from src.models.observer_manager import ObserverManager


import tkinter as tk

from src.views.widget.treeview_utils import DefaultTreeViewStyleManager


class AppState:
    def __init__(self, log_widget):
        # self._state = {}  ## 필요 없으면 나중에 삭제
        self.observer_manager = ObserverManager()
        self.notify_targets = []
        self.DefaultTreeViewStyleManager = DefaultTreeViewStyleManager
        # self.treeDataManager = TreeDataManager(self, related_widget)

        self.current_tab = None
        self.previous_tab = None  # Track the previous tab
        self.config = None

        self.selectedWMs = []
        self.selectedGWMitems = []
        self.selected_matchedWMs = []
        self.current_building = tk.StringVar()
        self.current_building.set("건물을 선택하세요")
        # self.selected_rvtTypes = []
        self.selected_rvtTypes = tk.StringVar()
        self.selected_rvtTypes_forLabel = tk.StringVar()

        self.switch_widget_status = tk.StringVar()
        self.suggest_area_open_status = True
        self.rvt_wm_isShort = True

        self.wm_group_data = {}
        self.lock_status = {}
        self.log_widget = log_widget
        self.clipboard_data = None  # 추가: 클립보드 데이터를 저장하는 필드

        self.team_std_info = {}
        # self.project_std_info = {}
        # self.project_apply_info = {}
        self.undo_stack = []

    def _notify_selected_change(self, *args):
        for noti_tgt in self.notify_targets:
            try:
                noti_tgt.update(self)
            except:
                pass

    ################### 옵저버 관련 #################################

    # 통합 상태 업데이트 함수
    ## 시트별 상태 업데이트 함수 - SGWM 시트의 내용을 state의 team_std_info에 업데이트

    def updateDB_total_data(self, data_kind, new_data):
        self.log_widget.write(f"update_{data_kind}_start\n")

        self.team_std_info.update({data_kind: new_data})

        self.log_widget.write(f"update_{data_kind}_data_end\n")

    def update_team_standard_info(self, new_data, data_kind=None):

        new_target_data = new_data.get(data_kind)
        self.updateDB_total_data(data_kind, new_target_data)

        # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
        self.observer_manager.notify_observers(self)

    # state 데이터 업데이트 함수들
    def match_wms_to_stdType(self, related_widget):
        print("match_wms_to_stdType_시작")
        data_kind = related_widget.data_kind
        selected_wms = go(
            self.selectedWMs,
            sorted,
            list,
        )
        print(selected_wms)
        related_widget.selected_item.get().split(" | ")
        grand_parent_item_name, parent_item_name, selected_item_name = (
            related_widget.selected_item.get().split(" | ")
        )

        # Use TreeDataNavigator to remove matched WMs
        treeDataManager = TreeDataManager_treeview(self, related_widget)
        treeDataManager.match_wms_to_stdType(
            data_kind,
            grand_parent_item_name,
            parent_item_name,
            selected_item_name,
            selected_wms,
        )

        print("match_wms_to_stdType_종료")

    def dematch_matchedWMs_to_stdType(self, related_widget):
        print("dematch_matchedWMs_to_stdType_시작")

        data_kind = related_widget.data_kind
        selected_matchedWMs = self.selected_matchedWMs

        # Split the selected item to get grandparent, parent, and selected item names
        grand_parent_item_name, parent_item_name, selected_item_name = (
            related_widget.selected_item.get().split(" | ")
        )

        # Use TreeDataNavigator to remove matched WMs
        navigator = TreeDataManager_treeview(self, related_widget)
        navigator.remove_matched_wms(
            data_kind,
            grand_parent_item_name,
            parent_item_name,
            selected_item_name,
            selected_matchedWMs,
        )

        print("dematch_matchedWMs_to_stdType_종료")

    def match_GWM_to_stdFam(self, related_widget):
        print("match_wms_to_stdType_시작")
        data_kind = related_widget.data_kind
        selectedGWMitems = go(
            self.selectedGWMitems,
            sorted,
            list,
        )
        print(f"!!!match_GWM_to_stdFam: {selectedGWMitems}")
        related_widget.selected_item.get().split(" | ")
        grandparent_item_name, parent_item_name, selected_item_name = (
            related_widget.selected_item.get().split(" | ")
        )

        # Use TreeDataNavigator to remove matched WMs
        treeDataManager = TreeDataManager_treeview(self, related_widget)
        treeDataManager.match_GWMitems_to_stdFam(
            data_kind,
            grandparent_item_name,
            parent_item_name,
            selected_item_name,
            selectedGWMitems,
        )

        print("match_wms_to_stdType_종료")
