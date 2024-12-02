# src/models/app_state.py
from src.controllers.tree_data_navigator import TreeDataManager
from src.controllers.widget.widgets import EditModeManager
from src.core.fp_utils import *
from src.models.observer_manager import ObserverManager


import tkinter as tk


class AppState:
    def __init__(self, log_widget):
        # self._state = {}  ## 필요 없으면 나중에 삭제
        self.observer_manager = ObserverManager()
        # self.treeDataManager = TreeDataManager(self, related_widget)

        self.current_tab = None
        self.previous_tab = None  # Track the previous tab
        self.config = None

        self.selectedWMs = []
        self.selected_matchedWMs = []

        self.wm_group_data = {}
        self.lock_status = {}
        self.log_widget = log_widget
        self.clipboard_data = None  # 추가: 클립보드 데이터를 저장하는 필드

        self.team_std_info = {}
        self.project_std_info = {}
        self.project_apply_info = {}
        self.undo_stack = []

    # def _notify_selected_change(self, *args):
    def _notify_selected_change(self, *args):
        try:
            self.std_matching_treeview_GWM.update(self)
        except:
            pass
        try:
            self.std_matching_treeview_SWM.update(self)
        except:
            pass

    ################### 옵저버 관련 #################################

    # 통합 상태 업데이트 함수
    ## 시트별 상태 업데이트 함수 - SGWM 시트의 내용을 state의 team_std_info에 업데이트

    def updateDB_total_data(self, data_kind, new_data):
        self.log_widget.write(f"update_{data_kind}_start\n")

        self.team_std_info.update({data_kind: new_data})

        self.log_widget.write(f"update_{data_kind}_data_end\n")

    def updateDB_WMs_data(self, new_data):
        self.log_widget.write("update_WMs_data_start\n")

        # self.project_info["GWM"] = new_data
        self.team_std_info.update({"WMs": new_data})
        # self.observer_manager.notify_observers()

        self.log_widget.write("update_WMs_data_end\n")

    def updateDB_S_GWM_data(self, new_data):
        self.log_widget.write("update_S_GWM_data_start\n")

        self.team_std_info.update({"std-GWM": new_data})

        self.log_widget.write("update_S_GWM_data_end\n")

    def updateDB_S_SWM_data(self, new_data):
        self.log_widget.write("update_S_SWM_data_start\n")

        self.team_std_info.update({"std-SWM": new_data})

        self.log_widget.write("update_S_SWM_data_end\n")

    def updateDB_commonInput_data(self, new_data):
        self.log_widget.write("update_S_SWM_data_start\n")

        self.team_std_info.update({"common-input": new_data})

        self.log_widget.write("update_S_SWM_data_end\n")

    def update_team_standard_info(self, new_data, data_kind=None):

        new_target_data = new_data.get(data_kind)
        self.updateDB_total_data(data_kind, new_target_data)

        # if data_kind == "std-GWM":
        #     new_target_data = new_data.get(data_kind)
        #     self.updateDB_S_GWM_data(new_target_data)
        # elif data_kind == "std-SWM":
        #     new_target_data = new_data.get(data_kind)
        #     self.updateDB_S_SWM_data(new_target_data)
        # elif data_kind == "common-input":
        #     new_target_data = new_data.get(data_kind)
        #     self.updateDB_commonInput_data(new_target_data)
        # elif data_kind == "WMs":
        #     new_WMs_data = new_data
        #     self.updateDB_WMs_data(new_WMs_data)

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
        treeDataManager = TreeDataManager(self, related_widget)
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
        navigator = TreeDataManager(self, related_widget)
        navigator.remove_matched_wms(
            data_kind,
            grand_parent_item_name,
            parent_item_name,
            selected_item_name,
            selected_matchedWMs,
        )

        print("dematch_matchedWMs_to_stdType_종료")

    # # 통합 상태 업데이트 함수
    # def update_project_info(self, new_data):
    #     self.project_info.update(new_data)
    #     self.observer_manager.notify_observers(self)

    # ################### 옵저버 관련 #################################

    # def __getitem__(self, key):
    #     return self._state.get(key)

    # def __setitem__(self, key, value):
    #     self._state[key] = value

    # # Add getter and setter for clipboard_data
    # def get_clipboard_data(self):
    #     return self.clipboard_data

    # def get_current_tab(self):
    #     """Return the currently selected tab."""
    #     return self.current_tab

    # def set_clipboard_data(self, data):
    #     self.clipboard_data = data

    # def set_current_tab(self, tab_name):
    #     self.current_tab = tab_name

    # def load_config(self, config_data):
    #     self.config = config_data

    # def update_wm_group_data(self, data):
    #     self.wm_group_data = data

    # def set_lock_status(self, item_name, status):
    #     self.lock_status[item_name] = status

    # def get_lock_status(self, item_name):
    #     return self.lock_status.get(item_name, False)

    # # Method to get and set previous tab
    # def get_previous_tab(self):
    #     return self.previous_tab

    # def set_previous_tab(self, tab_name):
    #     self.previous_tab = tab_name
